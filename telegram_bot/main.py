#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Warmly Telegram Bot
Telegram бот для мотивации и поддержки с тёплыми словами
"""

import asyncio
import json
import random
import signal
import sys
from datetime import datetime, time
from typing import Dict, List, Optional

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, 
    MessageHandler, filters, ContextTypes
)
from telegram.constants import ParseMode

from database import Database
from scheduler import NotificationScheduler
from phrases import Phrases
from config import config
from logger import get_logger, log_startup, log_shutdown, log_error, log_user_action, log_bot_action

# Настройка логирования
logger = get_logger()

class WarmlyBot:
    def __init__(self, token: str = None):
        self.token = token or config.TELEGRAM_BOT_TOKEN
        if not self.token:
            raise ValueError("Токен бота не установлен")
        
        self.db = Database()
        self.scheduler = NotificationScheduler()
        self.phrases = Phrases()
        self.application = None
        self.running = False
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        user_id = update.effective_user.id
        username = update.effective_user.username or "друг"
        
        log_user_action(user_id, "Команда /start", f"Пользователь: {username}")
        
        # Регистрируем пользователя
        await self.db.add_user(user_id, username)
        
        welcome_text = f"""
🤍 Привет, {username}!

Добро пожаловать в Warmly — твоё ежедневное напоминание: ты достаточно хорош. Прямо сейчас.

Я буду отправлять тебе тёплые слова и поддержку в течение дня. Ты можешь:
• Получить мотивационную фразу
• Поделиться своим настроением
• Посмотреть архив сохранённых фраз
• Настроить время уведомлений

Начнём? ✨
        """
        
        keyboard = [
            [InlineKeyboardButton("💬 Получить фразу", callback_data="get_phrase")],
            [InlineKeyboardButton("😊 Как настроение?", callback_data="mood")],
            [InlineKeyboardButton("📚 Архив", callback_data="archive")],
            [InlineKeyboardButton("⚙️ Настройки", callback_data="settings")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_text, 
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /help"""
        help_text = """
🤍 <b>Warmly Bot - Помощь</b>

<b>Основные команды:</b>
/start - Начать работу с ботом
/help - Показать эту справку
/phrase - Получить мотивационную фразу
/mood - Поделиться настроением
/archive - Посмотреть сохранённые фразы
/settings - Настройки уведомлений

<b>Как пользоваться:</b>
• Нажми "Получить фразу" для мотивации
• Выбери "Как настроение?" чтобы поделиться чувствами
• Сохраняй понравившиеся фразы в архив
• Настрой время уведомлений в настройках

<b>О боте:</b>
Warmly — это твоё место для поддержки и добрых слов. 
Ты достаточно хорош просто тем, что есть. 💙
        """
        await update.message.reply_text(help_text, parse_mode=ParseMode.HTML)
    
    async def phrase_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /phrase"""
        await self.send_phrase(update, context)
    
    async def send_phrase(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Отправить мотивационную фразу"""
        user_id = update.effective_user.id
        current_hour = datetime.now().hour
        
        # Определяем время суток
        if 5 <= current_hour < 12:
            phrase = random.choice(self.phrases.morning_phrases)
            greeting = "Доброе утро 🌞"
        elif 20 <= current_hour or current_hour < 5:
            phrase = random.choice(self.phrases.evening_phrases)
            greeting = "Спокойной ночи 🌙"
        else:
            phrase = random.choice(self.phrases.day_phrases)
            greeting = "Тёплого дня ✨"
        
        message_text = f"{greeting}\n\n{phrase}"
        
        keyboard = [
            [InlineKeyboardButton("❤️ Сохранить в архив", callback_data=f"save_phrase:{phrase}")],
            [InlineKeyboardButton("📤 Поделиться", callback_data=f"share_phrase:{phrase}")],
            [InlineKeyboardButton("🔄 Ещё фразу", callback_data="get_phrase")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                message_text, 
                reply_markup=reply_markup,
                parse_mode=ParseMode.HTML
            )
        else:
            await update.message.reply_text(
                message_text, 
                reply_markup=reply_markup,
                parse_mode=ParseMode.HTML
            )
    
    async def mood_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /mood"""
        await self.show_mood_menu(update, context)
    
    async def show_mood_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать меню выбора настроения"""
        text = "Как ты себя чувствуешь? 😊"
        
        keyboard = [
            [InlineKeyboardButton("😊 Хорошо", callback_data="mood_good")],
            [InlineKeyboardButton("😐 Нормально", callback_data="mood_ok")],
            [InlineKeyboardButton("😞 Плохо", callback_data="mood_bad")],
            [InlineKeyboardButton("🔙 Назад", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                text, 
                reply_markup=reply_markup,
                parse_mode=ParseMode.HTML
            )
        else:
            await update.message.reply_text(
                text, 
                reply_markup=reply_markup,
                parse_mode=ParseMode.HTML
            )
    
    async def handle_mood_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE, mood: str):
        """Обработка выбора настроения"""
        user_id = update.effective_user.id
        
        if mood == "good":
            phrase = random.choice(self.phrases.good_mood_phrases)
        elif mood == "ok":
            phrase = random.choice(self.phrases.ok_mood_phrases)
        else:  # bad
            phrase = random.choice(self.phrases.bad_mood_phrases)
        
        message_text = f"<i>{phrase}</i>"
        
        keyboard = [
            [InlineKeyboardButton("❤️ Сохранить в архив", callback_data=f"save_phrase:{phrase}")],
            [InlineKeyboardButton("🔙 Назад", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(
            message_text, 
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
    
    async def archive_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /archive"""
        await self.show_archive(update, context)
    
    async def show_archive(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать архив сохранённых фраз"""
        user_id = update.effective_user.id
        saved_phrases = await self.db.get_saved_phrases(user_id)
        
        if not saved_phrases:
            text = "📚 <b>Архив</b>\n\nЗдесь будут жить твои любимые фразы. Нажми ❤, чтобы сохранить."
            keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="main_menu")]]
        else:
            text = "📚 <b>Твои сохранённые фразы:</b>\n\n"
            for i, phrase in enumerate(saved_phrases[:10], 1):  # Показываем первые 10
                text += f"{i}. {phrase}\n\n"
            
            if len(saved_phrases) > 10:
                text += f"... и ещё {len(saved_phrases) - 10} фраз"
            
            keyboard = [
                [InlineKeyboardButton("🗑 Очистить архив", callback_data="clear_archive")],
                [InlineKeyboardButton("🔙 Назад", callback_data="main_menu")]
            ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                text, 
                reply_markup=reply_markup,
                parse_mode=ParseMode.HTML
            )
        else:
            await update.message.reply_text(
                text, 
                reply_markup=reply_markup,
                parse_mode=ParseMode.HTML
            )
    
    async def settings_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /settings"""
        await self.show_settings(update, context)
    
    async def show_settings(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать настройки"""
        user_id = update.effective_user.id
        user_settings = await self.db.get_user_settings(user_id)
        
        morning_time = user_settings.get('morning_time', '08:00')
        evening_time = user_settings.get('evening_time', '22:00')
        morning_enabled = user_settings.get('morning_enabled', True)
        evening_enabled = user_settings.get('evening_enabled', True)
        
        text = f"""
⚙️ <b>Настройки</b>

🌅 <b>Утренние уведомления:</b> {'✅' if morning_enabled else '❌'} {morning_time}
🌙 <b>Вечерние уведомления:</b> {'✅' if evening_enabled else '❌'} {evening_time}

Выбери, что хочешь настроить:
        """
        
        keyboard = [
            [InlineKeyboardButton(f"🌅 Утро {'✅' if morning_enabled else '❌'}", callback_data="toggle_morning")],
            [InlineKeyboardButton(f"🌙 Вечер {'✅' if evening_enabled else '❌'}", callback_data="toggle_evening")],
            [InlineKeyboardButton("🔙 Назад", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                text, 
                reply_markup=reply_markup,
                parse_mode=ParseMode.HTML
            )
        else:
            await update.message.reply_text(
                text, 
                reply_markup=reply_markup,
                parse_mode=ParseMode.HTML
            )
    
    async def show_main_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать главное меню"""
        text = "🤍 <b>Warmly</b>\n\nВыбери, что хочешь сделать:"
        
        keyboard = [
            [InlineKeyboardButton("💬 Получить фразу", callback_data="get_phrase")],
            [InlineKeyboardButton("😊 Как настроение?", callback_data="mood")],
            [InlineKeyboardButton("📚 Архив", callback_data="archive")],
            [InlineKeyboardButton("⚙️ Настройки", callback_data="settings")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(
            text, 
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик нажатий на кнопки"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        if data == "get_phrase":
            await self.send_phrase(update, context)
        elif data == "mood":
            await self.show_mood_menu(update, context)
        elif data == "archive":
            await self.show_archive(update, context)
        elif data == "settings":
            await self.show_settings(update, context)
        elif data == "main_menu":
            await self.show_main_menu(update, context)
        elif data.startswith("mood_"):
            mood = data.split("_")[1]
            await self.handle_mood_selection(update, context, mood)
        elif data.startswith("save_phrase:"):
            phrase = data.split(":", 1)[1]
            await self.save_phrase(update, context, phrase)
        elif data.startswith("share_phrase:"):
            phrase = data.split(":", 1)[1]
            await self.share_phrase(update, context, phrase)
        elif data == "clear_archive":
            await self.clear_archive(update, context)
        elif data == "toggle_morning":
            await self.toggle_morning_notifications(update, context)
        elif data == "toggle_evening":
            await self.toggle_evening_notifications(update, context)
    
    async def save_phrase(self, update: Update, context: ContextTypes.DEFAULT_TYPE, phrase: str):
        """Сохранить фразу в архив"""
        user_id = update.effective_user.id
        await self.db.save_phrase(user_id, phrase)
        
        await update.callback_query.answer("Фраза сохранена в архив! ❤️")
    
    async def share_phrase(self, update: Update, context: ContextTypes.DEFAULT_TYPE, phrase: str):
        """Поделиться фразой"""
        share_text = f"🤍 Warmly\n\n{phrase}\n\nОтправлено через @warmly_bot"
        await update.callback_query.answer(f"Скопируй и отправь другу:\n\n{share_text}")
    
    async def clear_archive(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Очистить архив"""
        user_id = update.effective_user.id
        await self.db.clear_saved_phrases(user_id)
        await update.callback_query.answer("Архив очищен")
        await self.show_archive(update, context)
    
    async def toggle_morning_notifications(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Переключить утренние уведомления"""
        user_id = update.effective_user.id
        current_settings = await self.db.get_user_settings(user_id)
        new_value = not current_settings.get('morning_enabled', True)
        await self.db.update_user_setting(user_id, 'morning_enabled', new_value)
        await update.callback_query.answer("Настройки обновлены")
        await self.show_settings(update, context)
    
    async def toggle_evening_notifications(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Переключить вечерние уведомления"""
        user_id = update.effective_user.id
        current_settings = await self.db.get_user_settings(user_id)
        new_value = not current_settings.get('evening_enabled', True)
        await self.db.update_user_setting(user_id, 'evening_enabled', new_value)
        await update.callback_query.answer("Настройки обновлены")
        await self.show_settings(update, context)
    
    async def send_scheduled_notification(self, user_id: int, notification_type: str):
        """Отправить запланированное уведомление"""
        if notification_type == "morning":
            phrase = random.choice(self.phrases.morning_phrases)
            greeting = "Доброе утро 🌞"
        else:  # evening
            phrase = random.choice(self.phrases.evening_phrases)
            greeting = "Спокойной ночи 🌙"
        
        message_text = f"{greeting}\n\n{phrase}"
        
        try:
            await self.application.bot.send_message(
                chat_id=user_id,
                text=message_text,
                parse_mode=ParseMode.HTML
            )
        except Exception as e:
            logger.error(f"Ошибка отправки уведомления пользователю {user_id}: {e}")
    
    def run(self):
        """Запустить бота"""
        try:
            log_startup()
            
            # Создаём приложение
            self.application = Application.builder().token(self.token).build()
            
            # Добавляем обработчики команд
            self.application.add_handler(CommandHandler("start", self.start_command))
            self.application.add_handler(CommandHandler("help", self.help_command))
            self.application.add_handler(CommandHandler("phrase", self.phrase_command))
            self.application.add_handler(CommandHandler("mood", self.mood_command))
            self.application.add_handler(CommandHandler("archive", self.archive_command))
            self.application.add_handler(CommandHandler("settings", self.settings_command))
            
            # Добавляем обработчик кнопок
            self.application.add_handler(CallbackQueryHandler(self.button_callback))
            
            # Настраиваем планировщик
            self.scheduler.set_bot_instance(self)
            self.scheduler.start()
            
            # Настраиваем обработку сигналов
            self._setup_signal_handlers()
            
            self.running = True
            log_bot_action("Бот запущен", "Ожидание сообщений...")
            
            # Запускаем бота
            self.application.run_polling()
            
        except Exception as e:
            log_error(e, "Ошибка при запуске бота")
            raise
        finally:
            self._shutdown()
    
    def _setup_signal_handlers(self):
        """Настройка обработчиков сигналов"""
        def signal_handler(signum, frame):
            log_bot_action("Получен сигнал завершения", f"Сигнал: {signum}")
            self._shutdown()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def _shutdown(self):
        """Корректное завершение работы бота"""
        if self.running:
            log_bot_action("Завершение работы бота", "Остановка сервисов...")
            self.running = False
            
            if self.scheduler:
                self.scheduler.stop()
            
            log_shutdown()

def main():
    """Главная функция"""
    try:
        # Проверяем конфигурацию
        config.validate()
        
        # Создаём и запускаем бота
        bot = WarmlyBot()
        bot.run()
        
    except ValueError as e:
        logger.error(f"Ошибка конфигурации: {e}")
        print(f"❌ Ошибка конфигурации: {e}")
        print("💡 Убедитесь, что установлен токен бота в переменной окружения TELEGRAM_BOT_TOKEN")
        sys.exit(1)
        
    except KeyboardInterrupt:
        logger.info("Получен сигнал прерывания")
        print("\n🤍 Бот остановлен пользователем")
        sys.exit(0)
        
    except Exception as e:
        log_error(e, "Критическая ошибка")
        print(f"❌ Критическая ошибка: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()