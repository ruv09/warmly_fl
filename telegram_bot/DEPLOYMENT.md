# 🚀 Развертывание Warmly Telegram Bot

## 📋 Варианты развертывания

### 1. Локальный запуск (для разработки)

```bash
# Клонирование репозитория
git clone <repository-url>
cd telegram_bot

# Установка зависимостей
pip install -r requirements.txt

# Настройка переменных окружения
cp .env.example .env
# Отредактируйте .env и добавьте токен

# Запуск
python main.py
```

### 2. Docker (рекомендуется для продакшена)

#### Создание Dockerfile:

```dockerfile
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . .

# Создаём пользователя для безопасности
RUN useradd --create-home --shell /bin/bash warmly
RUN chown -R warmly:warmly /app
USER warmly

# Устанавливаем переменные окружения
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Команда запуска
CMD ["python", "main.py"]
```

#### Создание docker-compose.yml:

```yaml
version: '3.8'

services:
  warmly-bot:
    build: .
    container_name: warmly-bot
    restart: unless-stopped
    environment:
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
      - LOG_LEVEL=INFO
      - DEFAULT_MORNING_TIME=08:00
      - DEFAULT_EVENING_TIME=22:00
      - DEFAULT_TIMEZONE=Europe/Moscow
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    networks:
      - warmly-network

  # Опционально: база данных PostgreSQL
  postgres:
    image: postgres:13
    container_name: warmly-postgres
    restart: unless-stopped
    environment:
      - POSTGRES_DB=warmly
      - POSTGRES_USER=warmly
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - warmly-network

volumes:
  postgres_data:

networks:
  warmly-network:
    driver: bridge
```

#### Запуск с Docker:

```bash
# Создание .env файла
echo "TELEGRAM_BOT_TOKEN=your_token_here" > .env
echo "POSTGRES_PASSWORD=your_password_here" >> .env

# Запуск
docker-compose up -d

# Просмотр логов
docker-compose logs -f warmly-bot

# Остановка
docker-compose down
```

### 3. Systemd (Linux сервер)

#### Создание сервиса:

```bash
sudo nano /etc/systemd/system/warmly-bot.service
```

```ini
[Unit]
Description=Warmly Telegram Bot
After=network.target
Wants=network.target

[Service]
Type=simple
User=warmly
Group=warmly
WorkingDirectory=/opt/warmly-bot
ExecStart=/usr/bin/python3 main.py
Restart=always
RestartSec=10
Environment=TELEGRAM_BOT_TOKEN=your_token_here
Environment=LOG_LEVEL=INFO
Environment=PYTHONPATH=/opt/warmly-bot

# Безопасность
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/opt/warmly-bot

# Логирование
StandardOutput=journal
StandardError=journal
SyslogIdentifier=warmly-bot

[Install]
WantedBy=multi-user.target
```

#### Управление сервисом:

```bash
# Создание пользователя
sudo useradd -r -s /bin/false warmly

# Создание директории
sudo mkdir -p /opt/warmly-bot
sudo chown warmly:warmly /opt/warmly-bot

# Копирование файлов
sudo cp -r . /opt/warmly-bot/
sudo chown -R warmly:warmly /opt/warmly-bot

# Активация сервиса
sudo systemctl daemon-reload
sudo systemctl enable warmly-bot
sudo systemctl start warmly-bot

# Проверка статуса
sudo systemctl status warmly-bot

# Просмотр логов
sudo journalctl -u warmly-bot -f
```

### 4. Heroku

#### Создание Procfile:

```
worker: python main.py
```

#### Создание runtime.txt:

```
python-3.9.16
```

#### Настройка переменных окружения:

```bash
heroku config:set TELEGRAM_BOT_TOKEN=your_token_here
heroku config:set LOG_LEVEL=INFO
```

#### Деплой:

```bash
# Установка Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Логин
heroku login

# Создание приложения
heroku create warmly-bot

# Деплой
git push heroku main

# Запуск воркера
heroku ps:scale worker=1

# Просмотр логов
heroku logs --tail
```

### 5. VPS (Ubuntu/Debian)

#### Установка зависимостей:

```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Python и pip
sudo apt install python3 python3-pip python3-venv -y

# Установка Git
sudo apt install git -y

# Создание пользователя
sudo useradd -m -s /bin/bash warmly
sudo usermod -aG sudo warmly
```

#### Настройка приложения:

```bash
# Переключение на пользователя
sudo su - warmly

# Клонирование репозитория
git clone <repository-url> warmly-bot
cd warmly-bot

# Создание виртуального окружения
python3 -m venv venv
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Настройка переменных окружения
cp .env.example .env
nano .env  # Добавьте токен
```

#### Настройка Nginx (опционально):

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🔧 Настройка мониторинга

### 1. Логирование

```bash
# Настройка ротации логов
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

### 2. Мониторинг системы

```bash
# Установка htop для мониторинга
sudo apt install htop -y

# Мониторинг ресурсов
htop
```

### 3. Автоматические бэкапы

```bash
# Создание скрипта бэкапа
sudo nano /opt/warmly-bot/backup.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/opt/backups/warmly-bot"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Бэкап базы данных
cp /opt/warmly-bot/warmly_bot.db $BACKUP_DIR/warmly_bot_$DATE.db

# Бэкап логов
tar -czf $BACKUP_DIR/logs_$DATE.tar.gz /opt/warmly-bot/logs/

# Удаление старых бэкапов (старше 7 дней)
find $BACKUP_DIR -name "*.db" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

```bash
# Сделать скрипт исполняемым
sudo chmod +x /opt/warmly-bot/backup.sh

# Добавить в crontab
sudo crontab -e
# Добавить строку:
# 0 2 * * * /opt/warmly-bot/backup.sh
```

## 🚨 Безопасность

### 1. Firewall

```bash
# Настройка UFW
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
```

### 2. SSL сертификаты

```bash
# Установка Certbot
sudo apt install certbot -y

# Получение сертификата
sudo certbot --nginx -d your-domain.com
```

### 3. Обновления безопасности

```bash
# Автоматические обновления безопасности
sudo apt install unattended-upgrades -y
sudo dpkg-reconfigure -plow unattended-upgrades
```

## 📊 Мониторинг производительности

### 1. Системные метрики

```bash
# Установка monitoring tools
sudo apt install htop iotop nethogs -y

# Мониторинг в реальном времени
htop
iotop
nethogs
```

### 2. Логи приложения

```bash
# Просмотр логов в реальном времени
tail -f /opt/warmly-bot/logs/warmly_bot.log

# Поиск ошибок
grep -i error /opt/warmly-bot/logs/warmly_bot.log
```

### 3. Мониторинг базы данных

```bash
# Проверка размера базы данных
ls -lh /opt/warmly-bot/warmly_bot.db

# Проверка целостности
sqlite3 /opt/warmly-bot/warmly_bot.db "PRAGMA integrity_check;"
```

## 🔄 Обновления

### 1. Обновление кода

```bash
# Остановка сервиса
sudo systemctl stop warmly-bot

# Создание бэкапа
sudo cp -r /opt/warmly-bot /opt/warmly-bot.backup.$(date +%Y%m%d)

# Обновление кода
cd /opt/warmly-bot
git pull origin main

# Установка новых зависимостей
source venv/bin/activate
pip install -r requirements.txt

# Запуск сервиса
sudo systemctl start warmly-bot
```

### 2. Откат изменений

```bash
# Остановка сервиса
sudo systemctl stop warmly-bot

# Восстановление из бэкапа
sudo rm -rf /opt/warmly-bot
sudo mv /opt/warmly-bot.backup.$(date +%Y%m%d) /opt/warmly-bot

# Запуск сервиса
sudo systemctl start warmly-bot
```

## 📞 Поддержка

### 1. Логи для диагностики

```bash
# Системные логи
sudo journalctl -u warmly-bot -f

# Логи приложения
tail -f /opt/warmly-bot/logs/warmly_bot.log

# Логи ошибок
tail -f /opt/warmly-bot/logs/warmly_bot_errors.log
```

### 2. Проверка состояния

```bash
# Статус сервиса
sudo systemctl status warmly-bot

# Проверка процессов
ps aux | grep python

# Проверка портов
netstat -tlnp | grep python
```

### 3. Восстановление после сбоев

```bash
# Перезапуск сервиса
sudo systemctl restart warmly-bot

# Проверка конфигурации
sudo systemctl daemon-reload

# Проверка прав доступа
sudo chown -R warmly:warmly /opt/warmly-bot
```

---

**Удачного развертывания! 🚀**