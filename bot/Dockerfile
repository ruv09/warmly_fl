# syntax=docker/dockerfile:1
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create non-root user
RUN useradd -m appuser
WORKDIR /app

# Install deps first for better caching
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy bot code
COPY . /app

# Runtime env (provide TELEGRAM_BOT_TOKEN at runtime)
ENV DB_PATH=/app/bot.db

USER appuser

CMD ["python", "-m", "bot.main"]
