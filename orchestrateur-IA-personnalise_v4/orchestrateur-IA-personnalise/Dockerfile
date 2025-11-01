# syntax=docker/dockerfile:1
FROM python:3.11-slim AS base
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

FROM base AS deps
COPY requirements.txt ./
RUN pip wheel --wheel-dir /wheels -r requirements.txt

FROM base AS runtime
COPY --from=deps /wheels /wheels
RUN pip install --no-index --find-links=/wheels /wheels/*
COPY . .
EXPOSE 8080
HEALTHCHECK CMD python -c "import socket; s=socket.socket(); s.connect(('127.0.0.1',8080)); print('ok')"
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8080"]
