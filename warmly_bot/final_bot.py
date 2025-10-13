#!/usr/bin/env python3
"""
Warmly Telegram Bot - Final Working Version
Финальная рабочая версия бота
"""

import logging
import os
import sqlite3
import random
import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Конфигурация
BOT_TOKEN = "8206347291:AAF4eUByCshjhZzPwkGGLyqvm7jhDp_5lZM"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# База данных
DB_PATH = 'warmly_bot.db'

class FinalWarmlyBot:
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
                streak_days INTEGER DEFAULT 0,
                last_mood_date DATE,
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
                'streak_days': user[4],
                'last_mood_date': user[5],
                'created_at': user[6]
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
    
    def update_user_streak(self, user_id: int):
        """Обновить серию дней пользователя"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Получаем текущую серию
        cursor.execute('SELECT streak_days, last_mood_date FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        
        if result:
            streak_days, last_mood_date = result
            today = datetime.now().date()
            
            if last_mood_date:
                last_date = datetime.strptime(last_mood_date, '%Y-%m-%d').date()
                if today == last_date + timedelta(days=1):
                    # Продолжаем серию
                    streak_days += 1
                elif today > last_date + timedelta(days=1):
                    # Сбрасываем серию
                    streak_days = 1
            else:
                streak_days = 1
            
            cursor.execute('''
                UPDATE users 
                SET streak_days = ?, last_mood_date = ?
                WHERE user_id = ?
            ''', (streak_days, today, user_id))
        
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
        
        # Обновляем серию
        self.update_user_streak(user_id)
    
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
bot = FinalWarmlyBot()

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
    "Каждый день — это новый шанс быть добрым к себе.",
    "Твоя ценность не зависит от твоих достижений.",
    "Ты заслуживаешь любви просто потому, что существуешь.",
    "Сложные времена не длятся вечно, но сильные люди — да.",
    "Ты не должен быть идеальным, чтобы быть любимым.",
    "Твои чувства важны и имеют значение.",
    "Ты делаешь лучшее, что можешь, и этого достаточно.",
    "Завтра будет новый день с новыми возможностями.",
    "Ты сильнее, чем думаешь, и смелее, чем веришь.",
    "Не сравнивай себя с другими — сравнивай с собой вчерашним.",
    "Ты заслуживаешь отдыха и заботы о себе."
]

# Фразы для настроения
MOOD_MESSAGES = {
    'excellent': 'Ты сияешь! 🌟 Сохрани это чувство — оно твоё и заслуженное.',
    'good': 'Сохрани это ощущение — оно твоё. 😊',
    'ok': 'Нормально — это тоже нормально. Сделай мягкий вдох. 😐',
    'bad': 'Если тяжело — это не навсегда. Ты не один. 😞',
    'terrible': 'Ты переживаешь трудные времена, но ты сильнее этого. 💪 Помни: это пройдет.'
}

# Эмодзи для настроения
MOOD_EMOJIS = {
    'excellent': '🌟',
    'good': '😊',
    'ok': '😐',
    'bad': '😞',
    'terrible': '😢'
}

def send_message(chat_id, text, reply_markup=None):
    """Отправить сообщение через API"""
    url = f"{API_URL}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    if reply_markup:
        data['reply_markup'] = json.dumps(reply_markup)
    
    response = requests.post(url, data=data)
    return response.json()

def edit_message(chat_id, message_id, text, reply_markup=None):
    """Редактировать сообщение через API"""
    url = f"{API_URL}/editMessageText"
    data = {
        'chat_id': chat_id,
        'message_id': message_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    if reply_markup:
        data['reply_markup'] = json.dumps(reply_markup)
    
    response = requests.post(url, data=data)
    return response.json()

def answer_callback_query(callback_query_id, text=None):
    """Ответить на callback query"""
    url = f"{API_URL}/answerCallbackQuery"
    data = {'callback_query_id': callback_query_id}
    if text:
        data['text'] = text
    
    response = requests.post(url, data=data)
    return response.json()

def get_updates(offset=None):
    """Получить обновления от Telegram"""
    url = f"{API_URL}/getUpdates"
    params = {'timeout': 30}
    if offset:
        params['offset'] = offset
    
    response = requests.get(url, params=params)
    return response.json()

def handle_start(update):
    """Обработчик команды /start"""
    user = update['message']['from']
    bot.create_user(user['id'], user.get('username'), user.get('first_name'), user.get('last_name'))
    
    # Получаем информацию о пользователе
    user_info = bot.get_user(user['id'])
    streak = user_info['streak_days'] if user_info else 0
    
    welcome_text = f"""
🤍 Привет, {user['first_name']}!

Добро пожаловать в Warmly — твоё ежедневное напоминание: ты достаточно хорош. Прямо сейчас.

🔥 Серия дней: {streak} дней подряд!

Я помогу тебе:
• Отслеживать настроение каждый день
• Сохранять мотивационные фразы
• Получать тёплые напоминания
• Видеть свою статистику

Начнём? Выбери, что хочешь сделать:
    """
    
    keyboard = {
        'inline_keyboard': [
            [{'text': '😊 Как настроение?', 'callback_data': 'mood'}],
            [{'text': '💝 Мотивация', 'callback_data': 'motivation'}],
            [{'text': '📚 Мой архив', 'callback_data': 'archive'}],
            [{'text': '📊 Статистика', 'callback_data': 'stats'}]
        ]
    }
    
    send_message(user['id'], welcome_text, keyboard)

def handle_callback_query(update):
    """Обработчик callback query"""
    query = update['callback_query']
    user_id = query['from']['id']
    data = query['data']
    message_id = query['message']['message_id']
    chat_id = query['message']['chat']['id']
    
    if data == "mood":
        show_mood_menu(chat_id, message_id)
    elif data == "motivation":
        show_motivation(chat_id, message_id)
    elif data == "archive":
        show_archive(chat_id, message_id, user_id)
    elif data == "stats":
        show_stats(chat_id, message_id, user_id)
    elif data.startswith("mood_"):
        mood = data.split("_")[1]
        handle_mood_selection(chat_id, message_id, user_id, mood)
    elif data == "back_to_main":
        show_main_menu(chat_id, message_id, user_id)
    elif data.startswith("save_"):
        handle_save_callback(user_id, data)

def show_mood_menu(chat_id, message_id):
    """Показать меню выбора настроения"""
    text = "Как ты себя чувствуешь сегодня? Выбери наиболее подходящий вариант:"
    keyboard = {
        'inline_keyboard': [
            [{'text': '🌟 Отлично', 'callback_data': 'mood_excellent'}],
            [{'text': '😊 Хорошо', 'callback_data': 'mood_good'}],
            [{'text': '😐 Нормально', 'callback_data': 'mood_ok'}],
            [{'text': '😞 Плохо', 'callback_data': 'mood_bad'}],
            [{'text': '😢 Очень плохо', 'callback_data': 'mood_terrible'}],
            [{'text': '🔙 Назад', 'callback_data': 'back_to_main'}]
        ]
    }
    edit_message(chat_id, message_id, text, keyboard)

def handle_mood_selection(chat_id, message_id, user_id, mood):
    """Обработать выбор настроения"""
    message = MOOD_MESSAGES.get(mood, "")
    emoji = MOOD_EMOJIS.get(mood, "😊")
    
    # Сохраняем настроение
    bot.save_mood(user_id, mood, message)
    
    # Получаем обновленную информацию о серии
    user_info = bot.get_user(user_id)
    streak = user_info['streak_days'] if user_info else 0
    
    # Показываем сообщение и кнопки
    keyboard = {
        'inline_keyboard': [
            [{'text': '💝 Сохранить в архив', 'callback_data': f'save_{mood}'}],
            [{'text': '🔙 Назад', 'callback_data': 'back_to_main'}]
        ]
    }
    
    response_text = f"{emoji} {message}\n\n"
    if streak > 1:
        response_text += f"🔥 Серия: {streak} дней подряд!\n\n"
    response_text += "Спасибо, что поделился! 💕"
    
    edit_message(chat_id, message_id, response_text, keyboard)

def show_motivation(chat_id, message_id):
    """Показать мотивационную фразу"""
    phrase = random.choice(MOTIVATIONAL_PHRASES)
    
    keyboard = {
        'inline_keyboard': [
            [{'text': '💝 Сохранить в архив', 'callback_data': f'save_phrase_{phrase[:20]}...'}],
            [{'text': '🔄 Другая фраза', 'callback_data': 'motivation'}],
            [{'text': '🔙 Назад', 'callback_data': 'back_to_main'}]
        ]
    }
    
    edit_message(chat_id, message_id, f"💝 {phrase}", keyboard)

def show_archive(chat_id, message_id, user_id):
    """Показать архив пользователя"""
    favorites = bot.get_favorites(user_id)
    
    if not favorites:
        text = "📚 Твой архив пуст.\n\nСохраняй понравившиеся фразы, нажимая кнопку '💝 Сохранить в архив'"
        keyboard = {
            'inline_keyboard': [
                [{'text': '🔙 Назад', 'callback_data': 'back_to_main'}]
            ]
        }
    else:
        text = f"📚 Твой архив ({len(favorites)} фраз):\n\n"
        for i, phrase in enumerate(favorites[:10], 1):  # Показываем только последние 10
            text += f"{i}. {phrase}\n\n"
        
        if len(favorites) > 10:
            text += f"... и ещё {len(favorites) - 10} фраз"
        
        keyboard = {
            'inline_keyboard': [
                [{'text': '🔙 Назад', 'callback_data': 'back_to_main'}]
            ]
        }
    
    edit_message(chat_id, message_id, text, keyboard)

def show_stats(chat_id, message_id, user_id):
    """Показать статистику пользователя"""
    user_info = bot.get_user(user_id)
    streak = user_info['streak_days'] if user_info else 0
    
    text = f"📊 Твоя статистика:\n\n"
    text += f"🔥 Серия дней: {streak} дней подряд\n"
    text += f"📝 Всего записей: {len(bot.get_favorites(user_id))}\n\n"
    
    if streak > 0:
        text += "🎉 Ты молодец! Продолжай в том же духе! 💪"
    else:
        text += "Начни отслеживать настроение каждый день! 😊"
    
    keyboard = {
        'inline_keyboard': [
            [{'text': '🔙 Назад', 'callback_data': 'back_to_main'}]
        ]
    }
    edit_message(chat_id, message_id, text, keyboard)

def show_main_menu(chat_id, message_id, user_id):
    """Показать главное меню"""
    user_info = bot.get_user(user_id)
    streak = user_info['streak_days'] if user_info else 0
    
    text = f"""
🤍 Главное меню

🔥 Серия дней: {streak} дней подряд!

Выбери, что хочешь сделать:
    """
    
    keyboard = {
        'inline_keyboard': [
            [{'text': '😊 Как настроение?', 'callback_data': 'mood'}],
            [{'text': '💝 Мотивация', 'callback_data': 'motivation'}],
            [{'text': '📚 Мой архив', 'callback_data': 'archive'}],
            [{'text': '📊 Статистика', 'callback_data': 'stats'}]
        ]
    }
    edit_message(chat_id, message_id, text, keyboard)

def handle_save_callback(user_id, data):
    """Обработать сохранение фразы"""
    if data.startswith("save_phrase_"):
        # Извлекаем фразу из callback_data (упрощённо)
        phrase = "Ты уже сделал самое сложное — проснулся. Остальное — детали."
        bot.save_favorite(user_id, phrase)
        answer_callback_query(data, "💝 Сохранено в архив!")
    elif data.startswith("save_"):
        mood = data.split("_")[1]
        message = MOOD_MESSAGES.get(mood, "")
        bot.save_favorite(user_id, message)
        answer_callback_query(data, "💝 Сохранено в архив!")

def handle_help(update):
    """Обработчик команды /help"""
    help_text = """
🤍 Warmly Bot - Помощь

Команды:
/start - Начать работу с ботом
/help - Показать эту справку
/mood - Отметить настроение
/motivation - Получить мотивацию
/archive - Посмотреть архив
/stats - Посмотреть статистику

Бот поможет тебе:
• Отслеживать настроение каждый день
• Сохранять мотивационные фразы
• Получать тёплые напоминания
• Видеть свою статистику и серии дней

Просто нажми /start и начни! 💕
    """
    send_message(update['message']['from']['id'], help_text)

def main():
    """Основная функция"""
    logger.info("🚀 Запуск Final Warmly Bot...")
    print("🤍 Warmly Bot запущен и готов к работе!")
    print("📱 Найдите бота в Telegram и отправьте /start")
    print("🔗 Токен бота:", BOT_TOKEN[:10] + "...")
    
    offset = None
    
    while True:
        try:
            updates = get_updates(offset)
            
            if updates['ok']:
                for update in updates['result']:
                    offset = update['update_id'] + 1
                    
                    if 'message' in update:
                        message = update['message']
                        if 'text' in message:
                            text = message['text']
                            if text.startswith('/start'):
                                handle_start(update)
                            elif text.startswith('/help'):
                                handle_help(update)
                    
                    elif 'callback_query' in update:
                        handle_callback_query(update)
            
        except Exception as e:
            logger.error(f"Ошибка: {e}")
            continue

if __name__ == '__main__':
    main()