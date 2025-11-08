# Dockerfile
FROM python:3.10-slim

# Не создаём .pyc и сразу пишем логи в stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Рабочая директория в контейнере
WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем всё остальное
COPY . .

# Порт, который откроет контейнер
EXPOSE 8000

# Запуск приложения (FastAPI)
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]
