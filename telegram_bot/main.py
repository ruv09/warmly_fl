#!/usr/bin/env python3
"""
Warmly Telegram Bot
Бот для отслеживания настроения и мотивации, основанный на Flutter приложении Warmly
"""

import logging
import os
import sqlite3
import json
from datetime import datetime, time
from typing import Dict, List, Optional
import schedule
import time as time_module
import threading

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, 
    MessageHandler, filters, ContextTypes
)
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Конфигурация
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в переменных окружения")

# База данных
DB_PATH = 'warmly_bot.db'

class WarmlyBot:
    def __init__(self):
        self.db_path = DB_PATH
        self.init_database()
        
    def init_database(self):
        """Инициализация базы данных"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Таблица пользователей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                timezone TEXT DEFAULT 'Europe/Moscow',
                alarm_time TEXT DEFAULT '07:30',
                alarm_enabled BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Таблица настроений
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS moods (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                mood TEXT NOT NULL,
                message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # Таблица избранных фраз
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS favorites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                phrase TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        """Получить информацию о пользователе"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                'user_id': user[0],
                'username': user[1],
                'first_name': user[2],
                'last_name': user[3],
                'timezone': user[4],
                'alarm_time': user[5],
                'alarm_enabled': bool(user[6]),
                'created_at': user[7]
            }
        return None
    
    def create_user(self, user_id: int, username: str = None, first_name: str = None, last_name: str = None):
        """Создать нового пользователя"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO users (user_id, username, first_name, last_name)
            VALUES (?, ?, ?, ?)
        ''', (user_id, username, first_name, last_name))
        conn.commit()
        conn.close()
    
    def save_mood(self, user_id: int, mood: str, message: str = None):
        """Сохранить настроение пользователя"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO moods (user_id, mood, message)
            VALUES (?, ?, ?)
        ''', (user_id, mood, message))
        conn.commit()
        conn.close()
    
    def save_favorite(self, user_id: int, phrase: str):
        """Сохранить фразу в избранное"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO favorites (user_id, phrase)
            VALUES (?, ?)
        ''', (user_id, phrase))
        conn.commit()
        conn.close()
    
    def get_favorites(self, user_id: int) -> List[str]:
        """Получить избранные фразы пользователя"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT phrase FROM favorites 
            WHERE user_id = ? 
            ORDER BY created_at DESC
        ''', (user_id,))
        favorites = [row[0] for row in cursor.fetchall()]
        conn.close()
        return favorites

# Глобальный экземпляр бота
bot = WarmlyBot()

# Мотивационные фразы
MOTIVATIONAL_PHRASES = [
    "Ты уже сделал самое сложное — проснулся. Остальное — детали.",
    "Ты — чудо. Просто так.",
    "Ты не один. Ты важен. Ты любим.",
    "Просто так — ты сегодня классный. Точка.",
    "ТыКлассный. Просто будучи собой 🤍",
    "Сохрани это ощущение — оно твоё.",
    "Нормально — это тоже нормально. Сделай мягкий вдох.",
    "Если тяжело — это не навсегда. Ты не один.",
    "Ты достаточно хорош. Прямо сейчас.",
    "Каждый день — это новый шанс быть добрым к себе."
]

# Фразы для настроения
MOOD_MESSAGES = {
    'good': 'Сохрани это ощущение — оно твоё. 😊',
    'ok': 'Нормально — это тоже нормально. Сделай мягкий вдох. 😐',
    'bad': 'Если тяжело — это не навсегда. Ты не один. 😞'
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user = update.effective_user
    bot.create_user(user.id, user.username, user.first_name, user.last_name)
    
    welcome_text = f"""
🤍 Привет, {user.first_name}!

Добро пожаловать в Warmly — твоё ежедневное напоминание: ты достаточно хорош. Прямо сейчас.

Я помогу тебе:
• Отслеживать настроение каждый день
• Сохранять мотивационные фразы
• Получать тёплые напоминания

Начнём? Выбери, что хочешь сделать:
    """
    
    keyboard = [
        [InlineKeyboardButton("😊 Как настроение?", callback_data="mood")],
        [InlineKeyboardButton("💝 Мотивация", callback_data="motivation")],
        [InlineKeyboardButton("📚 Мой архив", callback_data="archive")],
        [InlineKeyboardButton("⚙️ Настройки", callback_data="settings")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик нажатий на кнопки"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "mood":
        await show_mood_menu(query, context)
    elif query.data == "motivation":
        await show_motivation(query, context)
    elif query.data == "archive":
        await show_archive(query, context)
    elif query.data == "settings":
        await show_settings(query, context)
    elif query.data.startswith("mood_"):
        mood = query.data.split("_")[1]
        await handle_mood_selection(query, context, mood)
    elif query.data == "back_to_main":
        await show_main_menu(query, context)

async def show_mood_menu(query, context):
    """Показать меню выбора настроения"""
    text = "Как ты себя чувствуешь сегодня? 😊"
    keyboard = [
        [InlineKeyboardButton("😊 Хорошо", callback_data="mood_good")],
        [InlineKeyboardButton("😐 Нормально", callback_data="mood_ok")],
        [InlineKeyboardButton("😞 Плохо", callback_data="mood_bad")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back_to_main")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup)

async def handle_mood_selection(query, context, mood):
    """Обработать выбор настроения"""
    user_id = query.from_user.id
    message = MOOD_MESSAGES.get(mood, "")
    
    # Сохраняем настроение
    bot.save_mood(user_id, mood, message)
    
    # Показываем сообщение и кнопки
    keyboard = [
        [InlineKeyboardButton("💝 Сохранить в архив", callback_data=f"save_{mood}")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back_to_main")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(f"{message}\n\nСпасибо, что поделился! 💕", reply_markup=reply_markup)

async def show_motivation(query, context):
    """Показать мотивационную фразу"""
    import random
    phrase = random.choice(MOTIVATIONAL_PHRASES)
    
    keyboard = [
        [InlineKeyboardButton("💝 Сохранить в архив", callback_data=f"save_phrase_{phrase[:20]}...")],
        [InlineKeyboardButton("🔄 Другая фраза", callback_data="motivation")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back_to_main")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(f"💝 {phrase}", reply_markup=reply_markup)

async def show_archive(query, context):
    """Показать архив пользователя"""
    user_id = query.from_user.id
    favorites = bot.get_favorites(user_id)
    
    if not favorites:
        text = "📚 Твой архив пуст.\n\nСохраняй понравившиеся фразы, нажимая кнопку '💝 Сохранить в архив'"
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="back_to_main")]]
    else:
        text = "📚 Твой архив:\n\n"
        for i, phrase in enumerate(favorites[:10], 1):  # Показываем только последние 10
            text += f"{i}. {phrase}\n\n"
        
        if len(favorites) > 10:
            text += f"... и ещё {len(favorites) - 10} фраз"
        
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="back_to_main")]]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup)

async def show_settings(query, context):
    """Показать настройки"""
    user = bot.get_user(query.from_user.id)
    alarm_status = "включены" if user and user['alarm_enabled'] else "выключены"
    
    text = f"""
⚙️ Настройки

🕐 Будильник: {alarm_status}
🌍 Часовой пояс: {user['timezone'] if user else 'Europe/Moscow'}
⏰ Время уведомлений: {user['alarm_time'] if user else '07:30'}

В разработке... 🚧
    """
    
    keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="back_to_main")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup)

async def show_main_menu(query, context):
    """Показать главное меню"""
    text = f"""
🤍 Главное меню

Выбери, что хочешь сделать:
    """
    
    keyboard = [
        [InlineKeyboardButton("😊 Как настроение?", callback_data="mood")],
        [InlineKeyboardButton("💝 Мотивация", callback_data="motivation")],
        [InlineKeyboardButton("📚 Мой архив", callback_data="archive")],
        [InlineKeyboardButton("⚙️ Настройки", callback_data="settings")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup)

async def handle_save_callback(query, context):
    """Обработать сохранение фразы"""
    data = query.data
    user_id = query.from_user.id
    
    if data.startswith("save_phrase_"):
        # Извлекаем фразу из callback_data (упрощённо)
        phrase = "Ты уже сделал самое сложное — проснулся. Остальное — детали."
        bot.save_favorite(user_id, phrase)
        await query.answer("💝 Сохранено в архив!")
    elif data.startswith("save_"):
        mood = data.split("_")[1]
        message = MOOD_MESSAGES.get(mood, "")
        bot.save_favorite(user_id, message)
        await query.answer("💝 Сохранено в архив!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    help_text = """
🤍 Warmly Bot - Помощь

Команды:
/start - Начать работу с ботом
/help - Показать эту справку
/mood - Отметить настроение
/motivation - Получить мотивацию
/archive - Посмотреть архив

Бот поможет тебе:
• Отслеживать настроение каждый день
• Сохранять мотивационные фразы
• Получать тёплые напоминания

Просто нажми /start и начни! 💕
    """
    await update.message.reply_text(help_text)

def run_scheduler():
    """Запуск планировщика уведомлений"""
    def send_morning_notifications():
        # Здесь будет логика отправки утренних уведомлений
        pass
    
    # Планируем отправку уведомлений каждый день в 7:30
    schedule.every().day.at("07:30").do(send_morning_notifications)
    
    while True:
        schedule.run_pending()
        time_module.sleep(60)

def main():
    """Основная функция"""
    # Создаём приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(CallbackQueryHandler(handle_save_callback, pattern="^save_"))
    
    # Запускаем планировщик в отдельном потоке
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    
    # Запускаем бота
    logger.info("Запуск Warmly Bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()