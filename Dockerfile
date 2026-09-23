FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PORT=8000
WORKDIR /app
COPY backend/requirements*.txt ./backend/
COPY graph/requirements*.txt ./graph/
RUN python -m pip install --no-cache-dir -r backend/requirements-assistant.txt
COPY backend/ ./backend/
COPY graph/ ./graph/
COPY ai_agent/ ./ai_agent/
COPY Frontend/dist/ ./Frontend/dist/
COPY TelegramBot/miniapp/ ./TelegramBot/miniapp/
RUN python -m backend.jury --check && useradd --uid 10001 --create-home appuser
USER appuser
EXPOSE 8000
CMD ["python", "-m", "backend.jury", "--host", "0.0.0.0"]
