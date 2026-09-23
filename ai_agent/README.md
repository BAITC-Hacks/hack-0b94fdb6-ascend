# Помощник аналитика Graph + AI

Реализация обновлена по SPEC_GRAPH_AI. Провайдер — только OpenAI по прямому запросу пользователя. Настройки NVIDIA/LLM_BASE_URL не добавлялись. Ключ хранится локально, в браузер и Git не передаётся.

## Запуск Windows

Из корня репозитория:

```bat
.\.venv\Scripts\python.exe -m pip install -r ai_agent/requirements.txt
.\.venv\Scripts\python.exe -m backend.run_pipeline --data "D:\Хакатон ИИ Агент\data" --config graph/config/methodology.yaml
.\.venv\Scripts\python.exe -m ai_agent --output backend/output --env-file ai_agent/.env --port 8001
```

Открыть http://127.0.0.1:8001/assistant и /analysis-extras. `--snapshot путь/snapshot.json` пригоден для отдельной проверки агента; остальные основные API backend в этом режиме читают собственный output. Для единого сайта используйте `--output`.

`ai_agent/.env` (исключён из Git):

```dotenv
ASSISTANT_ENABLED=1
OPENAI_API_KEY=your-secret-key
OPENAI_MODEL=gpt-4.1-mini
```

Файл читается только при `--env-file`, переменные процесса приоритетнее. Без ключа, модели, флага либо при сбое OpenAI работает локальный разбор с `mode:fallback`, а не ошибка отключения. Сам ключ не нужен для графа, выгрузок, карточек и дополнительных анализов.

## Возможности

16 инструментов только для чтения: get_node, get_neighbors, common_downstream, common_upstream, find_paths, get_top, find_nodes, get_cluster, get_temporal, get_routes, get_anomalies, get_resilience, get_gaps, get_boundary, get_methodology, get_node_card. Они работают с готовым снимком; parquet в агенте не читается. Результат инструмента ограничен 8000 символами JSON, указывается source и truncated. Полные API и CSV не ограничены этим бюджетом модели.

GID — строки. Неизвестный узел возвращает понятную ошибку инструмента. Фильтры перечислены явно, SQL и исполняемый код не принимаются. Основные финансовые поля и основания выводятся из фактов инструментов. Вопрос о группе различает общее пересечение и частичную достижимость. Суммы кандидатов — их полный наблюдаемый оборот, не атрибуция денег выбранной группе.

Цикл: до 6 ответов модели, до 24 суммарных вызовов инструментов; независимые вызовы разрешены в одном ответе. Таймаут вызова 30 секунд, общий 60. Повтор плохих аргументов ограничен одним исправлением. История — последние 6 текстовых сообщений. GPT-4.1-mini использует температуру 0.1; модели без поддержки этого параметра получают запрос без него. Responses API: store=False, сохранение reasoning items внутри цикла. Основание — [официальная документация function calling](https://developers.openai.com/api/docs/guides/function-calling). store=False не является заявлением об отсутствии всех служебных логов у провайдера.

Guard проверяет точные GID, запрещённые формулировки и числа ≥1000 с допуском округления 1%, включая тыс/млн. Любое неподтверждённое большое число требует исправления (строже минимального порога SPEC); после одной неудачной попытки используется помеченный fallback по фактам. Это не доказательство семантической истинности: первичные выписки и границы наблюдения остаются обязательными для интерпретации.

Ответ API: `{answer,gids,tool_calls:[{name,args,ok,ms}],warnings,mode:"ai"|"fallback",run_id}`. Header X-Analysis-Run-Id тоже содержит снимок. Локальный разбор возвращает реальные операции, карточки, топ, пути, время, циклы, аномалии, устойчивость и запросы данных по распознанному типу вопроса. Неизвестные вопросы получают примеры поддерживаемых запросов. Личность, юридические выводы и изменение ролей не поддерживаются.

## Подключение в frontend

Использовать ui/AssistantPanel.tsx или:

```html
<script src="/ai-agent/assistant.js" defer></script>
<moneygraph-assistant api-base="/api/v1"></moneygraph-assistant>
```

Событие graph-node-select содержит detail.gid. Свяжите его с выбором узла и сбросом скрывающего фильтра; preventDefault отменяет переход по стандартной ссылке. Vite должен проксировать /api и /ai-agent. Показывайте mode=fallback и warnings, не блокируйте чат только потому, что assistant_enabled=false: локальный режим доступен при готовом снимке. Ожидание HTTP — не меньше 65 секунд. Наш виджет это уже делает; компонент основного frontend принадлежит его владельцу.

Дополнительные API и разделение обязанностей — [документ Graph](../graph/docs/SPEC_IMPLEMENTATION.md). Обязательная карточка детерминированная; необязательная AI-перефразировка ai=1 пока возвращает template с предупреждением.

## Проверки

```bat
.\.venv\Scripts\python.exe -m pytest graph/tests ai_agent/tests backend/tests -q
.\.venv\Scripts\python.exe -m ai_agent.evaluate --snapshot check-result/snapshot.json --output ai_agent/docs/assistant_eval_offline.md
.\.venv\Scripts\python.exe -m ai_agent.evaluate --snapshot check-result/snapshot.json --env-file ai_agent/.env --live --output ai_agent/docs/assistant_eval.md
```

Последняя команда явно выполняет платные запросы. Результаты: [локальный набор](docs/assistant_eval_offline.md), [живой OpenAI](docs/assistant_eval.md). Примеры и ожидаемые GID выбираются из переданного снимка; тест не подгоняет роли или пороги.
