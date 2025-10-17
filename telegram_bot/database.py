#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль для работы с базой данных
"""

import sqlite3
import json
import logging
from typing import List, Dict, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_path: str = "warmly_bot.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Инициализация базы данных"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Таблица пользователей
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Таблица сохранённых фраз
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS saved_phrases (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    phrase TEXT NOT NULL,
                    saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            """)
            
            # Таблица настроек пользователей
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_settings (
                    user_id INTEGER PRIMARY KEY,
                    morning_enabled BOOLEAN DEFAULT 1,
                    evening_enabled BOOLEAN DEFAULT 1,
                    morning_time TEXT DEFAULT '08:00',
                    evening_time TEXT DEFAULT '22:00',
                    timezone TEXT DEFAULT 'Europe/Moscow',
                    language TEXT DEFAULT 'ru',
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            """)
            
            # Таблица статистики
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_stats (
                    user_id INTEGER PRIMARY KEY,
                    phrases_received INTEGER DEFAULT 0,
                    phrases_saved INTEGER DEFAULT 0,
                    mood_checks INTEGER DEFAULT 0,
                    last_phrase_date DATE,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            """)
            
            conn.commit()
            logger.info("База данных инициализирована")
    
    async def add_user(self, user_id: int, username: str = None, 
                      first_name: str = None, last_name: str = None):
        """Добавить пользователя"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Проверяем, существует ли пользователь
            cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
            if cursor.fetchone():
                # Обновляем время последней активности
                cursor.execute("""
                    UPDATE users 
                    SET last_activity = CURRENT_TIMESTAMP,
                        username = COALESCE(?, username),
                        first_name = COALESCE(?, first_name),
                        last_name = COALESCE(?, last_name)
                    WHERE user_id = ?
                """, (username, first_name, last_name, user_id))
            else:
                # Добавляем нового пользователя
                cursor.execute("""
                    INSERT INTO users (user_id, username, first_name, last_name)
                    VALUES (?, ?, ?, ?)
                """, (user_id, username, first_name, last_name))
                
                # Создаём настройки по умолчанию
                cursor.execute("""
                    INSERT INTO user_settings (user_id)
                    VALUES (?)
                """, (user_id,))
                
                # Создаём статистику
                cursor.execute("""
                    INSERT INTO user_stats (user_id)
                    VALUES (?)
                """, (user_id,))
            
            conn.commit()
            logger.info(f"Пользователь {user_id} добавлен/обновлён")
    
    async def save_phrase(self, user_id: int, phrase: str):
        """Сохранить фразу в архив пользователя"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO saved_phrases (user_id, phrase)
                VALUES (?, ?)
            """, (user_id, phrase))
            
            # Обновляем статистику
            cursor.execute("""
                UPDATE user_stats 
                SET phrases_saved = phrases_saved + 1
                WHERE user_id = ?
            """, (user_id,))
            
            conn.commit()
            logger.info(f"Фраза сохранена для пользователя {user_id}")
    
    async def get_saved_phrases(self, user_id: int, limit: int = 50) -> List[str]:
        """Получить сохранённые фразы пользователя"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT phrase FROM saved_phrases
                WHERE user_id = ?
                ORDER BY saved_at DESC
                LIMIT ?
            """, (user_id, limit))
            
            phrases = [row[0] for row in cursor.fetchall()]
            return phrases
    
    async def clear_saved_phrases(self, user_id: int):
        """Очистить архив пользователя"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                DELETE FROM saved_phrases WHERE user_id = ?
            """, (user_id,))
            
            conn.commit()
            logger.info(f"Архив очищен для пользователя {user_id}")
    
    async def get_user_settings(self, user_id: int) -> Dict[str, Any]:
        """Получить настройки пользователя"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT morning_enabled, evening_enabled, morning_time, 
                       evening_time, timezone, language
                FROM user_settings
                WHERE user_id = ?
            """, (user_id,))
            
            row = cursor.fetchone()
            if row:
                return {
                    'morning_enabled': bool(row[0]),
                    'evening_enabled': bool(row[1]),
                    'morning_time': row[2],
                    'evening_time': row[3],
                    'timezone': row[4],
                    'language': row[5]
                }
            else:
                # Возвращаем настройки по умолчанию
                return {
                    'morning_enabled': True,
                    'evening_enabled': True,
                    'morning_time': '08:00',
                    'evening_time': '22:00',
                    'timezone': 'Europe/Moscow',
                    'language': 'ru'
                }
    
    async def update_user_setting(self, user_id: int, setting: str, value: Any):
        """Обновить настройку пользователя"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute(f"""
                UPDATE user_settings 
                SET {setting} = ?
                WHERE user_id = ?
            """, (value, user_id))
            
            conn.commit()
            logger.info(f"Настройка {setting} обновлена для пользователя {user_id}")
    
    async def get_users_for_notification(self, notification_type: str) -> List[int]:
        """Получить список пользователей для отправки уведомлений"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            if notification_type == "morning":
                enabled_field = "morning_enabled"
            else:  # evening
                enabled_field = "evening_enabled"
            
            cursor.execute(f"""
                SELECT user_id FROM user_settings
                WHERE {enabled_field} = 1
            """)
            
            user_ids = [row[0] for row in cursor.fetchall()]
            return user_ids
    
    async def update_user_stats(self, user_id: int, stat_type: str, increment: int = 1):
        """Обновить статистику пользователя"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            if stat_type == "phrases_received":
                cursor.execute("""
                    UPDATE user_stats 
                    SET phrases_received = phrases_received + ?,
                        last_phrase_date = CURRENT_DATE
                    WHERE user_id = ?
                """, (increment, user_id))
            elif stat_type == "mood_checks":
                cursor.execute("""
                    UPDATE user_stats 
                    SET mood_checks = mood_checks + ?
                    WHERE user_id = ?
                """, (increment, user_id))
            
            conn.commit()
    
    async def get_user_stats(self, user_id: int) -> Dict[str, Any]:
        """Получить статистику пользователя"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT phrases_received, phrases_saved, mood_checks, last_phrase_date
                FROM user_stats
                WHERE user_id = ?
            """, (user_id,))
            
            row = cursor.fetchone()
            if row:
                return {
                    'phrases_received': row[0],
                    'phrases_saved': row[1],
                    'mood_checks': row[2],
                    'last_phrase_date': row[3]
                }
            else:
                return {
                    'phrases_received': 0,
                    'phrases_saved': 0,
                    'mood_checks': 0,
                    'last_phrase_date': None
                }
    
    async def get_all_users(self) -> List[Dict[str, Any]]:
        """Получить всех пользователей"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT user_id, username, first_name, last_name, created_at, last_activity
                FROM users
                ORDER BY created_at DESC
            """)
            
            users = []
            for row in cursor.fetchall():
                users.append({
                    'user_id': row[0],
                    'username': row[1],
                    'first_name': row[2],
                    'last_name': row[3],
                    'created_at': row[4],
                    'last_activity': row[5]
                })
            
            return users