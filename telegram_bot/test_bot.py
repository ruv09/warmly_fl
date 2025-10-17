#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тестирование Warmly Telegram Bot
"""

import asyncio
import unittest
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime, time
import tempfile
import os

# Импортируем модули бота
from database import Database
from phrases import Phrases
from scheduler import NotificationScheduler
from config import config

class TestDatabase(unittest.TestCase):
    """Тесты для модуля базы данных"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        # Создаём временную базу данных
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db.close()
        self.db = Database(self.temp_db.name)
    
    def tearDown(self):
        """Очистка после каждого теста"""
        os.unlink(self.temp_db.name)
    
    async def test_add_user(self):
        """Тест добавления пользователя"""
        user_id = 123456789
        username = "test_user"
        
        await self.db.add_user(user_id, username)
        
        # Проверяем, что пользователь добавлен
        users = await self.db.get_all_users()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0]['user_id'], user_id)
        self.assertEqual(users[0]['username'], username)
    
    async def test_save_phrase(self):
        """Тест сохранения фразы"""
        user_id = 123456789
        phrase = "Тестовая фраза"
        
        await self.db.add_user(user_id, "test_user")
        await self.db.save_phrase(user_id, phrase)
        
        # Проверяем, что фраза сохранена
        phrases = await self.db.get_saved_phrases(user_id)
        self.assertEqual(len(phrases), 1)
        self.assertEqual(phrases[0], phrase)
    
    async def test_user_settings(self):
        """Тест настроек пользователя"""
        user_id = 123456789
        
        await self.db.add_user(user_id, "test_user")
        
        # Получаем настройки по умолчанию
        settings = await self.db.get_user_settings(user_id)
        self.assertTrue(settings['morning_enabled'])
        self.assertTrue(settings['evening_enabled'])
        
        # Обновляем настройку
        await self.db.update_user_setting(user_id, 'morning_enabled', False)
        
        # Проверяем обновление
        updated_settings = await self.db.get_user_settings(user_id)
        self.assertFalse(updated_settings['morning_enabled'])

class TestPhrases(unittest.TestCase):
    """Тесты для модуля фраз"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        self.phrases = Phrases()
    
    def test_get_random_phrase(self):
        """Тест получения случайной фразы"""
        phrase = self.phrases.get_random_phrase("morning")
        self.assertIsInstance(phrase, str)
        self.assertGreater(len(phrase), 0)
        self.assertIn(phrase, self.phrases.morning_phrases)
    
    def test_phrase_categories(self):
        """Тест категорий фраз"""
        categories = ["morning", "day", "evening", "good", "ok", "bad"]
        
        for category in categories:
            phrase = self.phrases.get_random_phrase(category)
            self.assertIsInstance(phrase, str)
            self.assertGreater(len(phrase), 0)
    
    def test_all_phrases(self):
        """Тест получения всех фраз"""
        all_phrases = self.phrases.get_all_phrases()
        
        self.assertIn("morning", all_phrases)
        self.assertIn("day", all_phrases)
        self.assertIn("evening", all_phrases)
        self.assertIn("good_mood", all_phrases)
        self.assertIn("ok_mood", all_phrases)
        self.assertIn("bad_mood", all_phrases)
        
        for category, phrases_list in all_phrases.items():
            self.assertIsInstance(phrases_list, list)
            self.assertGreater(len(phrases_list), 0)

class TestScheduler(unittest.TestCase):
    """Тесты для планировщика"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        self.scheduler = NotificationScheduler()
    
    def test_scheduler_initialization(self):
        """Тест инициализации планировщика"""
        self.assertFalse(self.scheduler.running)
        self.assertIsNone(self.scheduler.thread)
        self.assertIsNone(self.scheduler.bot_instance)
        self.assertIsNone(self.scheduler.db)
    
    def test_set_bot_instance(self):
        """Тест установки экземпляра бота"""
        mock_bot = Mock()
        mock_db = Mock()
        mock_bot.db = mock_db
        
        self.scheduler.set_bot_instance(mock_bot)
        
        self.assertEqual(self.scheduler.bot_instance, mock_bot)
        self.assertEqual(self.scheduler.db, mock_db)

class TestConfig(unittest.TestCase):
    """Тесты для конфигурации"""
    
    def test_config_validation(self):
        """Тест валидации конфигурации"""
        # Тест с валидной конфигурацией
        with patch.dict(os.environ, {'TELEGRAM_BOT_TOKEN': '123456789:ABCdefGHIjklMNOpqrsTUVwxyz'}):
            config = Config()
            self.assertTrue(config.validate())
    
    def test_config_validation_invalid_token(self):
        """Тест валидации с неверным токеном"""
        with patch.dict(os.environ, {'TELEGRAM_BOT_TOKEN': 'invalid_token'}):
            config = Config()
            with self.assertRaises(ValueError):
                config.validate()
    
    def test_config_validation_missing_token(self):
        """Тест валидации без токена"""
        with patch.dict(os.environ, {}, clear=True):
            config = Config()
            with self.assertRaises(ValueError):
                config.validate()

class TestBotIntegration(unittest.TestCase):
    """Интеграционные тесты бота"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db.close()
        self.db = Database(self.temp_db.name)
    
    def tearDown(self):
        """Очистка после каждого теста"""
        os.unlink(self.temp_db.name)
    
    async def test_user_workflow(self):
        """Тест полного workflow пользователя"""
        user_id = 123456789
        username = "test_user"
        
        # 1. Регистрация пользователя
        await self.db.add_user(user_id, username)
        
        # 2. Получение настроек
        settings = await self.db.get_user_settings(user_id)
        self.assertTrue(settings['morning_enabled'])
        
        # 3. Сохранение фразы
        phrase = "Тестовая мотивационная фраза"
        await self.db.save_phrase(user_id, phrase)
        
        # 4. Получение сохранённых фраз
        saved_phrases = await self.db.get_saved_phrases(user_id)
        self.assertEqual(len(saved_phrases), 1)
        self.assertEqual(saved_phrases[0], phrase)
        
        # 5. Обновление статистики
        await self.db.update_user_stats(user_id, "phrases_received", 1)
        await self.db.update_user_stats(user_id, "phrases_saved", 1)
        
        # 6. Получение статистики
        stats = await self.db.get_user_stats(user_id)
        self.assertEqual(stats['phrases_received'], 1)
        self.assertEqual(stats['phrases_saved'], 1)
    
    async def test_notification_users(self):
        """Тест получения пользователей для уведомлений"""
        # Добавляем пользователей с разными настройками
        await self.db.add_user(1, "user1")
        await self.db.add_user(2, "user2")
        await self.db.add_user(3, "user3")
        
        # Отключаем утренние уведомления для пользователя 2
        await self.db.update_user_setting(2, 'morning_enabled', False)
        
        # Отключаем вечерние уведомления для пользователя 3
        await self.db.update_user_setting(3, 'evening_enabled', False)
        
        # Проверяем утренние уведомления
        morning_users = await self.db.get_users_for_notification("morning")
        self.assertIn(1, morning_users)
        self.assertNotIn(2, morning_users)
        self.assertIn(3, morning_users)
        
        # Проверяем вечерние уведомления
        evening_users = await self.db.get_users_for_notification("evening")
        self.assertIn(1, evening_users)
        self.assertIn(2, evening_users)
        self.assertNotIn(3, evening_users)

def run_async_test(test_func):
    """Запуск асинхронного теста"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(test_func())
    finally:
        loop.close()

def run_tests():
    """Запуск всех тестов"""
    print("🧪 Запуск тестов Warmly Telegram Bot")
    print("=" * 50)
    
    # Создаём тестовый набор
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Добавляем тесты
    suite.addTests(loader.loadTestsFromTestCase(TestDatabase))
    suite.addTests(loader.loadTestsFromTestCase(TestPhrases))
    suite.addTests(loader.loadTestsFromTestCase(TestScheduler))
    suite.addTests(loader.loadTestsFromTestCase(TestConfig))
    suite.addTests(loader.loadTestsFromTestCase(TestBotIntegration))
    
    # Запускаем тесты
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Выводим результаты
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("✅ Все тесты прошли успешно!")
    else:
        print(f"❌ Тесты завершились с ошибками: {len(result.failures)} failures, {len(result.errors)} errors")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    # Запускаем тесты
    success = run_tests()
    
    # Запускаем асинхронные тесты
    print("\n🔄 Запуск асинхронных тестов...")
    
    async def run_async_tests():
        test_db = TestDatabase()
        test_db.setUp()
        try:
            await test_db.test_add_user()
            await test_db.test_save_phrase()
            await test_db.test_user_settings()
            print("✅ Асинхронные тесты базы данных прошли успешно")
        finally:
            test_db.tearDown()
        
        test_integration = TestBotIntegration()
        test_integration.setUp()
        try:
            await test_integration.test_user_workflow()
            await test_integration.test_notification_users()
            print("✅ Интеграционные тесты прошли успешно")
        finally:
            test_integration.tearDown()
    
    run_async_test(run_async_tests)
    
    print("\n🎉 Тестирование завершено!")