# Dockerfile
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

# Dépendances
COPY requirements.txt .
RUN python -m pip install -U pip wheel && pip install -r requirements.txt

# Code
COPY . .

# Port et démarrage
EXPOSE 8080
CMD ["uvicorn", "engine.api.main:app", "--host", "0.0.0.0", "--port", "8080"]
