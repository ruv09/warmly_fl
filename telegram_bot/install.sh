#!/bin/bash

# Скрипт установки Warmly Telegram Bot

echo "🤍 Установка Warmly Telegram Bot..."

# Проверяем наличие Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 не найден. Пожалуйста, установите Python 3.8 или выше."
    exit 1
fi

# Проверяем версию Python
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Требуется Python 3.8 или выше. Текущая версия: $python_version"
    exit 1
fi

echo "✅ Python $python_version найден"

# Создаём виртуальное окружение
echo "📦 Создание виртуального окружения..."
python3 -m venv venv

# Активируем виртуальное окружение
echo "🔧 Активация виртуального окружения..."
source venv/bin/activate

# Обновляем pip
echo "⬆️ Обновление pip..."
pip install --upgrade pip

# Устанавливаем зависимости
echo "📚 Установка зависимостей..."
pip install -r requirements.txt

# Создаём файл .env если его нет
if [ ! -f .env ]; then
    echo "⚙️ Создание файла конфигурации..."
    cp .env.example .env
    echo "📝 Пожалуйста, отредактируйте файл .env и добавьте токен вашего бота"
fi

echo ""
echo "🎉 Установка завершена!"
echo ""
echo "📋 Следующие шаги:"
echo "1. Получите токен бота у @BotFather в Telegram"
echo "2. Отредактируйте файл .env и добавьте токен"
echo "3. Запустите бота командой: python main.py"
echo ""
echo "📖 Подробная документация в файле README.md"
echo ""
echo "🤍 Удачи с вашим ботом!"