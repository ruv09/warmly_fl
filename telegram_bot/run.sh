#!/bin/bash

# Скрипт запуска Warmly Telegram Bot

echo "🤍 Запуск Warmly Telegram Bot..."

# Проверяем наличие виртуального окружения
if [ ! -d "venv" ]; then
    echo "❌ Виртуальное окружение не найдено. Запустите install.sh сначала."
    exit 1
fi

# Активируем виртуальное окружение
echo "🔧 Активация виртуального окружения..."
source venv/bin/activate

# Проверяем наличие файла .env
if [ ! -f .env ]; then
    echo "❌ Файл .env не найден. Создайте его на основе .env.example"
    exit 1
fi

# Загружаем переменные окружения
export $(cat .env | grep -v '^#' | xargs)

# Проверяем наличие токена
if [ -z "$TELEGRAM_BOT_TOKEN" ] || [ "$TELEGRAM_BOT_TOKEN" = "your_bot_token_here" ]; then
    echo "❌ Токен бота не настроен. Отредактируйте файл .env"
    exit 1
fi

echo "✅ Конфигурация проверена"
echo "🚀 Запуск бота..."

# Запускаем бота
python main.py