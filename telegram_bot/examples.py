#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Примеры использования Warmly Telegram Bot
"""

import asyncio
import random
from datetime import datetime, time
from typing import List, Dict

from database import Database
from phrases import Phrases
from scheduler import NotificationScheduler

class BotExamples:
    """Примеры использования компонентов бота"""
    
    def __init__(self):
        self.db = Database()
        self.phrases = Phrases()
        self.scheduler = NotificationScheduler()
    
    async def example_user_registration(self):
        """Пример регистрации пользователя"""
        print("📝 Пример регистрации пользователя")
        
        user_id = 123456789
        username = "example_user"
        first_name = "Иван"
        last_name = "Петров"
        
        await self.db.add_user(user_id, username, first_name, last_name)
        print(f"✅ Пользователь {username} зарегистрирован")
    
    async def example_save_phrase(self):
        """Пример сохранения фразы"""
        print("💾 Пример сохранения фразы")
        
        user_id = 123456789
        phrase = "Ты достаточно хорош просто тем, что есть."
        
        await self.db.save_phrase(user_id, phrase)
        print(f"✅ Фраза сохранена: {phrase}")
    
    async def example_get_saved_phrases(self):
        """Пример получения сохранённых фраз"""
        print("📚 Пример получения сохранённых фраз")
        
        user_id = 123456789
        phrases = await self.db.get_saved_phrases(user_id)
        
        print(f"✅ Найдено {len(phrases)} фраз:")
        for i, phrase in enumerate(phrases, 1):
            print(f"  {i}. {phrase}")
    
    async def example_get_random_phrase(self):
        """Пример получения случайной фразы"""
        print("🎲 Пример получения случайной фразы")
        
        # Получаем фразу в зависимости от времени суток
        current_hour = datetime.now().hour
        
        if 5 <= current_hour < 12:
            phrase = random.choice(self.phrases.morning_phrases)
            time_of_day = "утро"
        elif 20 <= current_hour or current_hour < 5:
            phrase = random.choice(self.phrases.evening_phrases)
            time_of_day = "вечер"
        else:
            phrase = random.choice(self.phrases.day_phrases)
            time_of_day = "день"
        
        print(f"✅ Фраза на {time_of_day}: {phrase}")
    
    async def example_mood_phrases(self):
        """Пример фраз для разных настроений"""
        print("😊 Пример фраз для разных настроений")
        
        moods = [
            ("good", "хорошее"),
            ("ok", "нормальное"),
            ("bad", "плохое")
        ]
        
        for mood, mood_name in moods:
            if mood == "good":
                phrase = random.choice(self.phrases.good_mood_phrases)
            elif mood == "ok":
                phrase = random.choice(self.phrases.ok_mood_phrases)
            else:
                phrase = random.choice(self.phrases.bad_mood_phrases)
            
            print(f"✅ {mood_name.capitalize()} настроение: {phrase}")
    
    async def example_user_settings(self):
        """Пример работы с настройками пользователя"""
        print("⚙️ Пример работы с настройками")
        
        user_id = 123456789
        
        # Получаем текущие настройки
        settings = await self.db.get_user_settings(user_id)
        print(f"📋 Текущие настройки: {settings}")
        
        # Обновляем настройку
        await self.db.update_user_setting(user_id, 'morning_enabled', False)
        print("✅ Утренние уведомления отключены")
        
        # Получаем обновлённые настройки
        new_settings = await self.db.get_user_settings(user_id)
        print(f"📋 Новые настройки: {new_settings}")
    
    async def example_statistics(self):
        """Пример работы со статистикой"""
        print("📊 Пример работы со статистикой")
        
        user_id = 123456789
        
        # Обновляем статистику
        await self.db.update_user_stats(user_id, "phrases_received", 5)
        await self.db.update_user_stats(user_id, "phrases_saved", 2)
        await self.db.update_user_stats(user_id, "mood_checks", 3)
        
        # Получаем статистику
        stats = await self.db.get_user_stats(user_id)
        print(f"📈 Статистика пользователя: {stats}")
    
    async def example_notification_scheduling(self):
        """Пример планирования уведомлений"""
        print("⏰ Пример планирования уведомлений")
        
        # Получаем пользователей для утренних уведомлений
        morning_users = await self.db.get_users_for_notification("morning")
        print(f"🌅 Пользователи для утренних уведомлений: {len(morning_users)}")
        
        # Получаем пользователей для вечерних уведомлений
        evening_users = await self.db.get_users_for_notification("evening")
        print(f"🌙 Пользователи для вечерних уведомлений: {len(evening_users)}")
    
    async def example_phrase_categories(self):
        """Пример работы с категориями фраз"""
        print("📝 Пример работы с категориями фраз")
        
        categories = [
            ("morning", "утренние"),
            ("day", "дневные"),
            ("evening", "вечерние"),
            ("good", "для хорошего настроения"),
            ("ok", "для нормального настроения"),
            ("bad", "для плохого настроения")
        ]
        
        for category, description in categories:
            phrase = self.phrases.get_random_phrase(category)
            print(f"✅ {description.capitalize()}: {phrase}")
    
    async def example_database_operations(self):
        """Пример различных операций с базой данных"""
        print("🗄️ Пример операций с базой данных")
        
        # Получаем всех пользователей
        users = await self.db.get_all_users()
        print(f"👥 Всего пользователей: {len(users)}")
        
        # Получаем статистику для каждого пользователя
        for user in users[:3]:  # Показываем только первых 3
            stats = await self.db.get_user_stats(user['user_id'])
            print(f"📊 Пользователь {user['username']}: {stats}")
    
    async def run_all_examples(self):
        """Запустить все примеры"""
        print("🤍 Запуск примеров Warmly Telegram Bot")
        print("=" * 50)
        
        try:
            await self.example_user_registration()
            print()
            
            await self.example_save_phrase()
            print()
            
            await self.example_get_saved_phrases()
            print()
            
            await self.example_get_random_phrase()
            print()
            
            await self.example_mood_phrases()
            print()
            
            await self.example_user_settings()
            print()
            
            await self.example_statistics()
            print()
            
            await self.example_notification_scheduling()
            print()
            
            await self.example_phrase_categories()
            print()
            
            await self.example_database_operations()
            print()
            
            print("✅ Все примеры выполнены успешно!")
            
        except Exception as e:
            print(f"❌ Ошибка при выполнении примеров: {e}")

async def main():
    """Главная функция для запуска примеров"""
    examples = BotExamples()
    await examples.run_all_examples()

if __name__ == "__main__":
    asyncio.run(main())