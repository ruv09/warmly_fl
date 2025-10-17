#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль для настройки логирования
"""

import logging
import logging.handlers
import os
import sys
from datetime import datetime
from typing import Optional

from config import config

class BotLogger:
    """Класс для настройки логирования бота"""
    
    def __init__(self, name: str = "warmly_bot"):
        self.name = name
        self.logger = logging.getLogger(name)
        self._setup_logger()
    
    def _setup_logger(self):
        """Настройка логгера"""
        # Очищаем существующие обработчики
        self.logger.handlers.clear()
        
        # Устанавливаем уровень логирования
        log_level = getattr(logging, config.LOG_LEVEL.upper(), logging.INFO)
        self.logger.setLevel(log_level)
        
        # Создаём форматтер
        formatter = logging.Formatter(
            config.LOG_FORMAT,
            datefmt=config.LOG_DATE_FORMAT
        )
        
        # Обработчик для консоли
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # Обработчик для файла (если указан)
        if config.LOG_FILE:
            # Создаём папку для логов, если её нет
            log_dir = os.path.dirname(config.LOG_FILE)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir)
            
            # Ротирующий файловый обработчик
            file_handler = logging.handlers.RotatingFileHandler(
                config.LOG_FILE,
                maxBytes=config.LOG_MAX_SIZE,
                backupCount=config.LOG_BACKUP_COUNT,
                encoding='utf-8'
            )
            file_handler.setLevel(log_level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
        
        # Обработчик для ошибок (отдельный файл)
        error_handler = logging.handlers.RotatingFileHandler(
            config.LOG_FILE.replace('.log', '_errors.log'),
            maxBytes=config.LOG_MAX_SIZE,
            backupCount=config.LOG_BACKUP_COUNT,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        self.logger.addHandler(error_handler)
        
        # Предотвращаем дублирование логов
        self.logger.propagate = False
    
    def get_logger(self) -> logging.Logger:
        """Получить настроенный логгер"""
        return self.logger
    
    def log_startup(self):
        """Логирование запуска бота"""
        self.logger.info("=" * 50)
        self.logger.info("🤍 Warmly Telegram Bot запускается...")
        self.logger.info(f"Время запуска: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.logger.info(f"Уровень логирования: {config.LOG_LEVEL}")
        self.logger.info(f"Режим разработки: {config.is_development()}")
        self.logger.info("=" * 50)
    
    def log_shutdown(self):
        """Логирование остановки бота"""
        self.logger.info("=" * 50)
        self.logger.info("🤍 Warmly Telegram Bot останавливается...")
        self.logger.info(f"Время остановки: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.logger.info("=" * 50)
    
    def log_user_action(self, user_id: int, action: str, details: str = ""):
        """Логирование действий пользователя"""
        self.logger.info(f"Пользователь {user_id}: {action} {details}")
    
    def log_error(self, error: Exception, context: str = ""):
        """Логирование ошибок"""
        self.logger.error(f"Ошибка {context}: {str(error)}", exc_info=True)
    
    def log_performance(self, operation: str, duration: float, details: str = ""):
        """Логирование производительности"""
        self.logger.info(f"Производительность: {operation} - {duration:.2f}с {details}")
    
    def log_notification(self, user_id: int, notification_type: str, success: bool):
        """Логирование уведомлений"""
        status = "успешно" if success else "неудачно"
        self.logger.info(f"Уведомление {notification_type} для пользователя {user_id}: {status}")
    
    def log_database_operation(self, operation: str, table: str, user_id: Optional[int] = None):
        """Логирование операций с базой данных"""
        user_info = f" (пользователь {user_id})" if user_id else ""
        self.logger.debug(f"БД: {operation} в таблице {table}{user_info}")
    
    def log_scheduler_event(self, event: str, details: str = ""):
        """Логирование событий планировщика"""
        self.logger.info(f"Планировщик: {event} {details}")
    
    def log_security_event(self, event: str, user_id: int, details: str = ""):
        """Логирование событий безопасности"""
        self.logger.warning(f"Безопасность: {event} от пользователя {user_id} {details}")
    
    def log_statistics(self, stats: dict):
        """Логирование статистики"""
        self.logger.info(f"Статистика: {stats}")
    
    def log_configuration(self):
        """Логирование конфигурации"""
        self.logger.info("Конфигурация бота:")
        self.logger.info(f"  - Токен: {'*' * 20}{config.TELEGRAM_BOT_TOKEN[-4:] if config.TELEGRAM_BOT_TOKEN else 'НЕ УСТАНОВЛЕН'}")
        self.logger.info(f"  - База данных: {config.DB_PATH}")
        self.logger.info(f"  - Логирование: {config.LOG_LEVEL}")
        self.logger.info(f"  - Режим разработки: {config.is_development()}")
        self.logger.info(f"  - Утренние уведомления: {config.DEFAULT_MORNING_TIME}")
        self.logger.info(f"  - Вечерние уведомления: {config.DEFAULT_EVENING_TIME}")
        self.logger.info(f"  - Часовой пояс: {config.DEFAULT_TIMEZONE}")

# Создаём глобальный экземпляр логгера
bot_logger = BotLogger()

def get_logger(name: str = None) -> logging.Logger:
    """Получить логгер"""
    if name:
        return logging.getLogger(name)
    return bot_logger.get_logger()

def log_exception(func):
    """Декоратор для логирования исключений"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            bot_logger.log_error(e, f"в функции {func.__name__}")
            raise
    return wrapper

def log_performance(func):
    """Декоратор для логирования производительности"""
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        try:
            result = func(*args, **kwargs)
            duration = (datetime.now() - start_time).total_seconds()
            bot_logger.log_performance(func.__name__, duration)
            return result
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            bot_logger.log_performance(func.__name__, duration, f"(ошибка: {str(e)})")
            raise
    return wrapper