#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Конфигурация бота
"""

import os
from typing import Dict, Any

class Config:
    """Класс конфигурации бота"""
    
    def __init__(self):
        # Основные настройки
        self.TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
        self.DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///warmly_bot.db')
        self.LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
        self.LOG_FILE = os.getenv('LOG_FILE', 'warmly_bot.log')
        
        # Настройки уведомлений
        self.DEFAULT_MORNING_TIME = os.getenv('DEFAULT_MORNING_TIME', '08:00')
        self.DEFAULT_EVENING_TIME = os.getenv('DEFAULT_EVENING_TIME', '22:00')
        self.DEFAULT_TIMEZONE = os.getenv('DEFAULT_TIMEZONE', 'Europe/Moscow')
        
        # Настройки базы данных
        self.DB_PATH = 'warmly_bot.db'
        self.MAX_SAVED_PHRASES = 100
        self.ARCHIVE_LIMIT = 50
        
        # Настройки бота
        self.BOT_USERNAME = None  # Будет установлено автоматически
        self.BOT_FIRST_NAME = None  # Будет установлено автоматически
        self.BOT_DESCRIPTION = "🤍 Warmly - твой персональный помощник для поддержки и мотивации"
        
        # Настройки сообщений
        self.MESSAGE_TIMEOUT = 30  # Таймаут для редактирования сообщений
        self.MAX_MESSAGE_LENGTH = 4096  # Максимальная длина сообщения Telegram
        
        # Настройки планировщика
        self.SCHEDULER_CHECK_INTERVAL = 60  # Интервал проверки в секундах
        self.NOTIFICATION_RETRY_ATTEMPTS = 3  # Количество попыток отправки уведомления
        
        # Настройки локализации
        self.SUPPORTED_LANGUAGES = ['ru', 'en']
        self.DEFAULT_LANGUAGE = 'ru'
        
        # Настройки статистики
        self.ENABLE_STATISTICS = True
        self.STATISTICS_RETENTION_DAYS = 365
        
        # Настройки безопасности
        self.MAX_MESSAGES_PER_MINUTE = 30  # Максимум сообщений в минуту от пользователя
        self.BLOCKED_USERS = []  # Список заблокированных пользователей
        
        # Настройки разработки
        self.DEBUG_MODE = os.getenv('DEBUG', 'False').lower() == 'true'
        self.DEVELOPER_MODE = os.getenv('DEVELOPER_MODE', 'False').lower() == 'true'
        
        # Настройки мониторинга
        self.ENABLE_HEALTH_CHECK = True
        self.HEALTH_CHECK_INTERVAL = 300  # 5 минут
        
        # Настройки резервного копирования
        self.BACKUP_ENABLED = True
        self.BACKUP_INTERVAL = 86400  # 24 часа
        self.BACKUP_RETENTION_DAYS = 7
        
        # Настройки уведомлений администратора
        self.ADMIN_USER_IDS = []  # ID администраторов для уведомлений
        self.ADMIN_NOTIFICATIONS = True
        
        # Настройки API (если будет добавлено в будущем)
        self.API_ENABLED = False
        self.API_PORT = 8080
        self.API_HOST = '0.0.0.0'
        
        # Настройки кэширования
        self.CACHE_ENABLED = True
        self.CACHE_TTL = 3600  # 1 час
        
        # Настройки логирования
        self.LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        self.LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
        self.LOG_MAX_SIZE = 10 * 1024 * 1024  # 10 MB
        self.LOG_BACKUP_COUNT = 5
        
        # Настройки базы данных
        self.DB_CONNECTION_TIMEOUT = 30
        self.DB_QUERY_TIMEOUT = 10
        self.DB_MAX_CONNECTIONS = 10
        
        # Настройки планировщика задач
        self.TASK_QUEUE_SIZE = 1000
        self.TASK_WORKER_COUNT = 4
        self.TASK_RETRY_DELAY = 60  # секунды
        
        # Настройки уведомлений
        self.NOTIFICATION_BATCH_SIZE = 10
        self.NOTIFICATION_DELAY = 1  # секунды между уведомлениями
        
        # Настройки фраз
        self.PHRASES_ROTATION_ENABLED = True
        self.PHRASES_ROTATION_INTERVAL = 86400  # 24 часа
        self.PHRASES_CACHE_SIZE = 1000
        
        # Настройки пользовательского интерфейса
        self.INLINE_KEYBOARD_TIMEOUT = 30
        self.CALLBACK_QUERY_TIMEOUT = 30
        self.MESSAGE_EDIT_TIMEOUT = 30
        
        # Настройки безопасности
        self.RATE_LIMIT_ENABLED = True
        self.RATE_LIMIT_WINDOW = 60  # секунды
        self.RATE_LIMIT_MAX_REQUESTS = 30
        
        # Настройки мониторинга производительности
        self.PERFORMANCE_MONITORING = True
        self.PERFORMANCE_LOG_INTERVAL = 300  # 5 минут
        
        # Настройки обновлений
        self.AUTO_UPDATE_ENABLED = False
        self.UPDATE_CHECK_INTERVAL = 86400  # 24 часа
        
        # Настройки интеграций
        self.EXTERNAL_APIS_ENABLED = False
        self.WEATHER_API_KEY = None
        self.NEWS_API_KEY = None
        
        # Настройки тестирования
        self.TEST_MODE = False
        self.TEST_USER_IDS = []
        self.MOCK_EXTERNAL_SERVICES = False
    
    def validate(self) -> bool:
        """Проверить корректность конфигурации"""
        if not self.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN не установлен")
        
        if not self.TELEGRAM_BOT_TOKEN.startswith(('1', '2', '3', '4', '5', '6', '7', '8', '9')):
            raise ValueError("Неверный формат TELEGRAM_BOT_TOKEN")
        
        if self.LOG_LEVEL not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
            raise ValueError("Неверный уровень логирования")
        
        if self.DEFAULT_LANGUAGE not in self.SUPPORTED_LANGUAGES:
            raise ValueError("Неподдерживаемый язык по умолчанию")
        
        return True
    
    def get_database_config(self) -> Dict[str, Any]:
        """Получить конфигурацию базы данных"""
        return {
            'path': self.DB_PATH,
            'timeout': self.DB_CONNECTION_TIMEOUT,
            'query_timeout': self.DB_QUERY_TIMEOUT,
            'max_connections': self.DB_MAX_CONNECTIONS
        }
    
    def get_logging_config(self) -> Dict[str, Any]:
        """Получить конфигурацию логирования"""
        return {
            'level': self.LOG_LEVEL,
            'format': self.LOG_FORMAT,
            'date_format': self.LOG_DATE_FORMAT,
            'file': self.LOG_FILE,
            'max_size': self.LOG_MAX_SIZE,
            'backup_count': self.LOG_BACKUP_COUNT
        }
    
    def get_scheduler_config(self) -> Dict[str, Any]:
        """Получить конфигурацию планировщика"""
        return {
            'check_interval': self.SCHEDULER_CHECK_INTERVAL,
            'retry_attempts': self.NOTIFICATION_RETRY_ATTEMPTS,
            'batch_size': self.NOTIFICATION_BATCH_SIZE,
            'delay': self.NOTIFICATION_DELAY
        }
    
    def is_development(self) -> bool:
        """Проверить, запущен ли бот в режиме разработки"""
        return self.DEBUG_MODE or self.DEVELOPER_MODE
    
    def is_production(self) -> bool:
        """Проверить, запущен ли бот в продакшене"""
        return not self.is_development()
    
    def get_user_limits(self) -> Dict[str, int]:
        """Получить лимиты для пользователей"""
        return {
            'max_messages_per_minute': self.MAX_MESSAGES_PER_MINUTE,
            'max_saved_phrases': self.MAX_SAVED_PHRASES,
            'archive_limit': self.ARCHIVE_LIMIT
        }

# Создаём глобальный экземпляр конфигурации
config = Config()

# Проверяем конфигурацию при импорте
try:
    config.validate()
except ValueError as e:
    print(f"Ошибка конфигурации: {e}")
    exit(1)