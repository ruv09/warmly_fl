# 🤍 Полное руководство по созданию Warmly Telegram Bot

## 📋 Содержание

1. [Введение](#введение)
2. [Установка и настройка](#установка-и-настройка)
3. [Создание бота в Telegram](#создание-бота-в-telegram)
4. [Настройка проекта](#настройка-проекта)
5. [Запуск бота](#запуск-бота)
6. [Использование](#использование)
7. [Развертывание](#развертывание)
8. [Мониторинг и поддержка](#мониторинг-и-поддержка)
9. [Расширение функциональности](#расширение-функциональности)

## Введение

**Warmly Telegram Bot** - это Telegram бот для мотивации и поддержки, созданный на основе Flutter приложения Warmly. Бот отправляет тёплые слова и мотивационные фразы в зависимости от времени суток и настроения пользователя.

### 🎯 Основные возможности

- 🌅 **Утренние мотивации** - добрые слова для начала дня
- 🌞 **Дневная поддержка** - фразы для поддержки в течение дня  
- 🌙 **Вечерние напоминания** - тёплые слова перед сном
- 😊 **Отслеживание настроения** - поделитесь, как дела, и получите поддержку
- 📚 **Архив фраз** - сохраняйте понравившиеся мотивационные фразы
- ⚙️ **Настройки уведомлений** - настройте время получения сообщений
- 🌍 **Многоязычность** - поддержка русского и английского языков

## Установка и настройка

### Требования

- Python 3.8 или выше
- pip (менеджер пакетов Python)
- Git (для клонирования репозитория)
- Telegram аккаунт (для создания бота)

### 1. Установка Python

#### Windows:
1. Скачайте Python с [python.org](https://www.python.org/downloads/)
2. Установите, обязательно отметьте "Add Python to PATH"
3. Проверьте установку: `python --version`

#### macOS:
```bash
# Через Homebrew
brew install python3

# Или скачайте с python.org
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

### 2. Клонирование репозитория

```bash
git clone <repository-url>
cd telegram_bot
```

### 3. Создание виртуального окружения

```bash
# Создание виртуального окружения
python -m venv venv

# Активация (Windows)
venv\Scripts\activate

# Активация (macOS/Linux)
source venv/bin/activate
```

### 4. Установка зависимостей

```bash
pip install -r requirements.txt
```

## Создание бота в Telegram

### 1. Получение токена

1. Откройте Telegram
2. Найдите @BotFather
3. Отправьте команду `/newbot`
4. Следуйте инструкциям:
   - Введите имя бота (например: "Warmly Bot")
   - Введите username бота (например: "warmly_support_bot")
5. Скопируйте полученный токен (выглядит как `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2. Настройка бота

Отправьте @BotFather следующие команды:

```
/setdescription
Твой персональный помощник для поддержки и мотивации. Получай тёплые слова каждый день! 🤍

/setabouttext
Warmly - бот для ежедневной поддержки и мотивации. Отправляет тёплые слова в зависимости от времени суток и настроения.

/setcommands
start - Начать работу с ботом
help - Показать справку
phrase - Получить мотивационную фразу
mood - Поделиться настроением
archive - Посмотреть сохранённые фразы
settings - Настройки уведомлений
```

## Настройка проекта

### 1. Создание файла конфигурации

```bash
cp .env.example .env
```

### 2. Редактирование .env

Откройте файл `.env` и добавьте токен:

```bash
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=ваш_токен_здесь

# Database Configuration
DATABASE_URL=sqlite:///warmly_bot.db

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=warmly_bot.log

# Notification Configuration
DEFAULT_MORNING_TIME=08:00
DEFAULT_EVENING_TIME=22:00
DEFAULT_TIMEZONE=Europe/Moscow
```

### 3. Проверка конфигурации

```bash
python -c "from config import config; print('Конфигурация загружена успешно')"
```

## Запуск бота

### 1. Автоматический запуск

```bash
# Сделать скрипты исполняемыми
chmod +x install.sh run.sh

# Запуск
./run.sh
```

### 2. Ручной запуск

```bash
python main.py
```

### 3. Проверка работы

1. Найдите вашего бота в Telegram по username
2. Отправьте команду `/start`
3. Проверьте, что бот отвечает

## Использование

### Основные команды

- `/start` - Начать работу с ботом
- `/help` - Показать справку
- `/phrase` - Получить мотивационную фразу
- `/mood` - Поделиться настроением
- `/archive` - Посмотреть сохранённые фразы
- `/settings` - Настройки уведомлений

### Интерфейс бота

#### Главное меню
```
🤍 Warmly

Выбери, что хочешь сделать:

[💬 Получить фразу]
[😊 Как настроение?]
[📚 Архив]
[⚙️ Настройки]
```

#### Фразы с действиями
```
Доброе утро 🌞

Ты уже сделал самое сложное — проснулся. Остальное — детали.

[❤️ Сохранить в архив] [📤 Поделиться] [🔄 Ещё фразу]
```

### Типы фраз

#### Утренние фразы (5:00-12:00)
- "Ты уже сделал самое сложное — проснулся. Остальное — детали."
- "Сегодня можно идти мягко. Ты не обязан спешить."
- "Доброе утро. Твоя ценность не зависит от достижений."

#### Дневные фразы (12:00-20:00)
- "Сделай вдох. Ты имеешь право на паузу."
- "Если тяжело — это нормально. Ты не один."
- "Ты достаточно хорош просто тем, что есть."

#### Вечерние фразы (20:00-5:00)
- "Сегодня ты сделал достаточно. Отдых — тоже достижение."
- "Спасибо себе за этот день. Ты справился."
- "Ночь — чтобы мягко отпустить. Спокойной тебе тишины."

## Развертывание

### 1. Docker (рекомендуется)

#### Создание Dockerfile:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

#### Создание docker-compose.yml:
```yaml
version: '3.8'
services:
  warmly-bot:
    build: .
    environment:
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
    volumes:
      - ./data:/app/data
    restart: unless-stopped
```

#### Запуск:
```bash
docker-compose up -d
```

### 2. Systemd (Linux)

#### Создание сервиса:
```bash
sudo nano /etc/systemd/system/warmly-bot.service
```

```ini
[Unit]
Description=Warmly Telegram Bot
After=network.target

[Service]
Type=simple
User=warmly
WorkingDirectory=/opt/warmly-bot
ExecStart=/usr/bin/python3 main.py
Restart=always
Environment=TELEGRAM_BOT_TOKEN=your_token_here

[Install]
WantedBy=multi-user.target
```

#### Управление:
```bash
sudo systemctl enable warmly-bot
sudo systemctl start warmly-bot
sudo systemctl status warmly-bot
```

### 3. Heroku

#### Создание Procfile:
```
worker: python main.py
```

#### Деплой:
```bash
heroku create warmly-bot
heroku config:set TELEGRAM_BOT_TOKEN=your_token_here
git push heroku main
heroku ps:scale worker=1
```

## Мониторинг и поддержка

### 1. Логирование

#### Просмотр логов:
```bash
# Системные логи (systemd)
sudo journalctl -u warmly-bot -f

# Логи приложения
tail -f warmly_bot.log

# Логи ошибок
tail -f warmly_bot_errors.log
```

#### Настройка ротации логов:
```bash
sudo nano /etc/logrotate.d/warmly-bot
```

```
/opt/warmly-bot/logs/*.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 644 warmly warmly
}
```

### 2. Мониторинг производительности

#### Системные метрики:
```bash
# CPU и память
htop

# Дисковое пространство
df -h

# Сетевые соединения
netstat -tlnp
```

#### Мониторинг базы данных:
```bash
# Размер базы данных
ls -lh warmly_bot.db

# Целостность базы данных
sqlite3 warmly_bot.db "PRAGMA integrity_check;"

# Статистика пользователей
sqlite3 warmly_bot.db "SELECT COUNT(*) FROM users;"
```

### 3. Резервное копирование

#### Автоматические бэкапы:
```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/opt/backups/warmly-bot"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Бэкап базы данных
cp warmly_bot.db $BACKUP_DIR/warmly_bot_$DATE.db

# Бэкап логов
tar -czf $BACKUP_DIR/logs_$DATE.tar.gz logs/

# Удаление старых бэкапов
find $BACKUP_DIR -name "*.db" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

#### Настройка cron:
```bash
# Добавить в crontab
0 2 * * * /opt/warmly-bot/backup.sh
```

## Расширение функциональности

### 1. Добавление новых фраз

Отредактируйте файл `phrases.py`:

```python
# Добавьте новые фразы в соответствующие списки
self.morning_phrases.extend([
    "Новая утренняя фраза",
    "Ещё одна мотивационная фраза"
])
```

### 2. Добавление новых команд

В файле `main.py` добавьте новый обработчик:

```python
async def new_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Новая команда"""
    await update.message.reply_text("Ответ на новую команду")

# В методе run() добавьте:
self.application.add_handler(CommandHandler("new", self.new_command))
```

### 3. Добавление новых языков

1. Создайте файл `strings_<lang>.json` в папке `assets/i18n/`
2. Добавьте язык в `config.py`:
```python
self.SUPPORTED_LANGUAGES = ['ru', 'en', 'es', 'fr']
```

### 4. Интеграция с внешними API

```python
import requests

async def get_weather_phrase(self, city: str):
    """Получить фразу на основе погоды"""
    # API вызов
    response = requests.get(f"https://api.weather.com/v1/current?q={city}")
    weather = response.json()
    
    if weather['condition'] == 'sunny':
        return "Солнечный день — повод для радости!"
    else:
        return "Дождливый день — повод для уюта."
```

### 5. Добавление аналитики

```python
async def track_user_action(self, user_id: int, action: str):
    """Отслеживание действий пользователя"""
    # Отправка в аналитический сервис
    analytics_data = {
        'user_id': user_id,
        'action': action,
        'timestamp': datetime.now().isoformat()
    }
    # Отправка данных
```

## Устранение неполадок

### 1. Бот не отвечает

**Проблема:** Бот не отвечает на команды

**Решение:**
1. Проверьте правильность токена
2. Убедитесь, что бот не заблокирован пользователем
3. Проверьте логи на наличие ошибок
4. Перезапустите бота

### 2. Ошибки базы данных

**Проблема:** Ошибки при работе с базой данных

**Решение:**
1. Проверьте права доступа к файлу базы данных
2. Проверьте целостность базы данных
3. Создайте резервную копию и пересоздайте базу

### 3. Уведомления не приходят

**Проблема:** Автоматические уведомления не отправляются

**Решение:**
1. Проверьте настройки уведомлений пользователя
2. Убедитесь, что планировщик запущен
3. Проверьте время на сервере
4. Проверьте логи планировщика

### 4. Высокое потребление ресурсов

**Проблема:** Бот потребляет много CPU или памяти

**Решение:**
1. Проверьте логи на наличие ошибок
2. Оптимизируйте запросы к базе данных
3. Увеличьте интервалы между проверками
4. Добавьте ограничения на количество пользователей

## Безопасность

### 1. Защита токена

- Никогда не коммитьте токен в репозиторий
- Используйте переменные окружения
- Регулярно обновляйте токен

### 2. Ограничение доступа

```python
# Ограничение частоты запросов
async def rate_limit_check(self, user_id: int):
    """Проверка лимита запросов"""
    # Реализация ограничения
    pass
```

### 3. Валидация входных данных

```python
async def validate_input(self, text: str):
    """Валидация пользовательского ввода"""
    if len(text) > 1000:
        raise ValueError("Слишком длинное сообщение")
    # Другие проверки
```

## Производительность

### 1. Оптимизация базы данных

```python
# Создание индексов
cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_id ON saved_phrases(user_id)")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_saved_at ON saved_phrases(saved_at)")
```

### 2. Кэширование

```python
import functools
import time

@functools.lru_cache(maxsize=100)
def get_cached_phrase(category: str):
    """Кэширование фраз"""
    return random.choice(phrases[category])
```

### 3. Асинхронная обработка

```python
async def process_notifications_async(self):
    """Асинхронная обработка уведомлений"""
    tasks = []
    for user_id in self.get_notification_users():
        task = asyncio.create_task(self.send_notification(user_id))
        tasks.append(task)
    
    await asyncio.gather(*tasks)
```

## Заключение

Warmly Telegram Bot - это мощный инструмент для ежедневной поддержки и мотивации пользователей. Следуя этому руководству, вы сможете создать, настроить и развернуть собственного бота для поддержки.

### Основные принципы:

1. **Простота** - интерфейс должен быть понятным
2. **Доброта** - каждый пользователь заслуживает поддержки
3. **Персонализация** - адаптация под потребности пользователя
4. **Надёжность** - стабильная работа 24/7

### Следующие шаги:

1. Изучите код и понимайте, как он работает
2. Настройте бота под свои потребности
3. Добавьте новые функции
4. Поделитесь с сообществом

**Удачи с вашим ботом! 🤍**

---

**Помните: вы достаточно хороши просто тем, что есть. 💙**