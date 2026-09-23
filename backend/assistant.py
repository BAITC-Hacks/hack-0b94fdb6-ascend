"""HTTP boundary for the Graph team's agent; optional imports stay lazy."""
import importlib.util
import os
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator
from starlette.responses import JSONResponse


class Message(BaseModel):
    model_config = ConfigDict(extra='forbid')
    role: Literal['user', 'assistant']
    content: str = Field(min_length=1, max_length=4000)


class Question(BaseModel):
    model_config = ConfigDict(extra='forbid')
    question: str = Field(min_length=1, max_length=4000)
    history: list[Message] = Field(default_factory=list, max_length=6)

    @field_validator('question')
    @classmethod
    def nonblank(cls, value):
        if not value.strip():
            raise ValueError('Пустой вопрос')
        return value.strip()


REQUEST_SCHEMA = Question.model_json_schema()
REQUEST_SCHEMA['properties']['history']['items'] = REQUEST_SCHEMA.pop('$defs')['Message']


def readiness():
    if os.getenv('ASSISTANT_ENABLED') != '1':
        return False, 'AI-ассистент выключен: задайте ASSISTANT_ENABLED=1 в backend/.env'
    if not os.getenv('OPENAI_API_KEY', '').strip():
        return False, 'Не задан OPENAI_API_KEY в backend/.env'
    if not os.getenv('OPENAI_MODEL', '').strip():
        return False, 'Не задан OPENAI_MODEL в backend/.env'
    if any(importlib.util.find_spec(name) is None for name in ['openai', 'graph', 'pandas', 'yaml', 'networkx', 'scipy', 'pyarrow']):
        return False, 'Установите зависимости backend/requirements-assistant.txt'
    return True, 'Настроен. Доступ к модели проверяется при отправке вопроса.'


def failure(code, message, status):
    return JSONResponse({'error': {'code': code, 'message': message, 'details': {}}}, status_code=status)


def build_agent(snapshot, **options):
    from graph.assistant import Assistant

    class IntegratedAssistant(Assistant):
        async def ask(self, question, history=None):
            successful = []
            dispatch = self.tools.dispatch

            def record(name, args):
                result = dispatch(name, args)
                successful.append((name, result))
                return result

            self.tools.dispatch = record
            try:
                result = await super().ask(question, history)
            finally:
                self.tools.dispatch = dispatch
            # The upstream financial report displays at most three cards. For a
            # single top selection, render the entire returned list, without
            # copying or relaxing validation of the model's numerical prose.
            if len(successful) == 1 and successful[0][0] == 'get_top':
                rows = successful[0][1]['items']
                lines = [f'Приоритетные узлы: показано {len(rows)} из {successful[0][1]["total"]}.']
                for node in rows:
                    lines.append(f"• #{node['gid']} — {node['role']}; приоритет {node['priority_score']}; "
                                 f"вход {node['in_kzt']} ₸; выход {node['out_kzt']} ₸.")
                if successful[0][1].get('truncated'):
                    lines.append('Показана только выбранная часть результатов.')
                lines.append('Роли — гипотезы для проверки; суммы относятся к наблюдаемому срезу данных.')
                result = dict(result, answer='\n'.join(lines), gids=[node['gid'] for node in rows], answer_source='tool_result')
            return result

    return IntegratedAssistant(snapshot, **options)


async def answer(request, get_snapshot):
    enabled, message = readiness()
    # SPEC_GRAPH_AI: missing provider credentials activate the local fallback.
    # Bind the request to one immutable published run before any await.
    snapshot = get_snapshot()
    agent = None
    try:
        body = bytearray()
        async for chunk in request.stream():
            body.extend(chunk)
            if len(body) > 128 * 1024:
                return failure('invalid_param', 'Слишком большой запрос', 400)
        try:
            payload = Question.model_validate_json(bytes(body))
        except (ValidationError, ValueError):
            return failure('invalid_param', 'Нужен вопрос 1–4000 символов и не более 6 сообщений истории (user/assistant)', 400)
        from graph.assistant import AssistantError
        agent = build_agent(snapshot.data)
        try:
            result = await agent.ask(payload.question, [item.model_dump() for item in payload.history])
            return dict(result, run_id=snapshot.data['run']['run_id'])
        except AssistantError as exc:
            return JSONResponse(exc.response(), status_code=exc.status)
    except Exception:
        # Do not send provider exceptions, credentials or request bodies to clients/logs.
        return failure('internal', 'Сервис ассистента временно недоступен', 500)
    finally:
        if agent is not None and agent.client is not None:
            try:
                await agent.client.close()
            except Exception:
                pass
