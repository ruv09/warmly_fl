#!/bin/bash

# Скрипт развертывания Warmly Bot

echo "🚀 Развертывание Warmly Bot..."

# Проверяем наличие .env файла
if [ ! -f .env ]; then
    echo "❌ Файл .env не найден!"
    echo "Скопируйте .env.example в .env и заполните необходимые переменные:"
    echo "cp .env.example .env"
    exit 1
fi

# Проверяем наличие BOT_TOKEN
if ! grep -q "BOT_TOKEN=" .env || grep -q "BOT_TOKEN=your_telegram_bot_token_here" .env; then
    echo "❌ BOT_TOKEN не настроен в .env файле!"
    echo "Получите токен у @BotFather и добавьте его в .env файл"
    exit 1
fi

echo "✅ Конфигурация проверена"

# Создаем директорию для данных
mkdir -p data

# Устанавливаем зависимости
echo "📦 Установка зависимостей..."
pip install -r requirements.txt

# Запускаем бота
echo "🤖 Запуск бота..."
python enhanced_main.py