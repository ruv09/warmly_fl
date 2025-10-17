import json
import os
import logging
from datetime import datetime, time
from typing import Dict, Any
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Константы
USERS_FILE = "users.json"
PHRASES_FILE = "phrases.json"
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в переменных окружения!")

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Планировщик для уведомлений
scheduler = AsyncIOScheduler()

# Загружаем фразы
with open(PHRASES_FILE, "r", encoding="utf-8") as f:
    phrases = json.load(f)

# Словарь для хранения настроек пользователей в памяти
user_settings: Dict[str, Dict[str, str]] = {}


def load_users() -> Dict[str, Dict[str, str]]:
    """Загружает настройки пользователей из файла"""
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Ошибка при загрузке users.json: {e}")
            return {}
    return {}


def save_users(users: Dict[str, Dict[str, str]]) -> None:
    """Сохраняет настройки пользователей в файл"""
    try:
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
        logger.info("Настройки пользователей сохранены")
    except IOError as e:
        logger.error(f"Ошибка при сохранении users.json: {e}")


def validate_time(time_str: str) -> bool:
    """Проверяет корректность формата времени ЧЧ:ММ"""
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False


def get_random_phrase(phrase_type: str) -> str:
    """Возвращает случайную фразу утром или вечером"""
    import random
    phrase_list = phrases.get(phrase_type, [])
    return random.choice(phrase_list) if phrase_list else "Хорошего дня! 🌟"


async def send_morning_message(user_id: str):
    """Отправляет утреннее сообщение пользователю"""
    try:
        phrase = get_random_phrase("morning")
        await bot.send_message(user_id, phrase)
        logger.info(f"Утреннее сообщение отправлено пользователю {user_id}")
    except Exception as e:
        logger.error(f"Ошибка при отправке утреннего сообщения пользователю {user_id}: {e}")


async def send_evening_message(user_id: str):
    """Отправляет вечернее сообщение пользователю"""
    try:
        phrase = get_random_phrase("evening")
        await bot.send_message(user_id, phrase)
        logger.info(f"Вечернее сообщение отправлено пользователю {user_id}")
    except Exception as e:
        logger.error(f"Ошибка при отправке вечернего сообщения пользователю {user_id}: {e}")


def schedule_user_notifications(user_id: str, wakeup_time: str, sleep_time: str):
    """Планирует уведомления для пользователя"""
    # Удаляем старые задачи для этого пользователя
    try:
        scheduler.remove_job(f"morning_{user_id}", jobstore=None)
        scheduler.remove_job(f"evening_{user_id}", jobstore=None)
    except:
        pass
    
    # Парсим время
    wakeup_hour, wakeup_minute = map(int, wakeup_time.split(":"))
    sleep_hour, sleep_minute = map(int, sleep_time.split(":"))
    
    # Планируем утренние уведомления
    scheduler.add_job(
        send_morning_message,
        CronTrigger(hour=wakeup_hour, minute=wakeup_minute),
        args=[user_id],
        id=f"morning_{user_id}",
        replace_existing=True
    )
    
    # Планируем вечерние уведомления
    scheduler.add_job(
        send_evening_message,
        CronTrigger(hour=sleep_hour, minute=sleep_minute),
        args=[user_id],
        id=f"evening_{user_id}",
        replace_existing=True
    )
    
    logger.info(f"Уведомления запланированы для пользователя {user_id}: утро {wakeup_time}, вечер {sleep_time}")


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    """Обработчик команды /start"""
    user_id = str(message.from_user.id)
    
    if user_id in user_settings:
        # Пользователь уже настроен
        settings = user_settings[user_id]
        wakeup = settings.get("wakeup_time", "не установлено")
        sleep = settings.get("sleep_time", "не установлено")
        
        await message.answer(
            f"Привет! 🌿\n\n"
            f"Ты уже настроен!\n"
            f"Утро: {wakeup} | Вечер: {sleep}\n\n"
            f"Просто напиши новое время, чтобы изменить.\n"
            f"Формат: ЧЧ:ММ (например, 07:30)"
        )
    else:
        # Новый пользователь
        await message.answer(
            "Привет! 🌿\n\n"
            "Я Warmly — твой ежедневный помощник для эмоциональной поддержки.\n"
            "Я буду присылать тебе тёплые фразы утром и вечером.\n\n"
            "Давай настроим твоё расписание!\n\n"
            "Во сколько ты обычно просыпаешься? (например, 07:00)"
        )


@dp.message_handler(lambda message: message.text and message.text.count(':') == 1 and len(message.text.split(':')) == 2)
async def handle_time_input(message: types.Message):
    """Обработчик ввода времени"""
    user_id = str(message.from_user.id)
    time_str = message.text
    
    if not validate_time(time_str):
        await message.answer("Неверный формат времени! Используй ЧЧ:ММ (например, 07:30)")
        return
    
    if user_id not in user_settings:
        # Первый раз - запрашиваем время пробуждения
        user_settings[user_id] = {"wakeup_time": time_str}
        await message.answer(
            f"Отлично! Утро: {time_str} 🌅\n\n"
            f"А во сколько ты обычно ложишься спать? (например, 23:00)"
        )
    else:
        # Обновляем настройки
        if "wakeup_time" in user_settings[user_id] and "sleep_time" not in user_settings[user_id]:
            # Устанавливаем время сна
            user_settings[user_id]["sleep_time"] = time_str
            wakeup = user_settings[user_id]["wakeup_time"]
            
            # Планируем уведомления
            schedule_user_notifications(user_id, wakeup, time_str)
            
            # Сохраняем в файл
            save_users(user_settings)
            
            await message.answer(
                f"Отлично! Настройки сохранены! 🌿\n\n"
                f"Утро: {wakeup} 🌅\n"
                f"Вечер: {time_str} 🌙\n\n"
                f"Я буду присылать тебе тёплые фразы в это время каждый день!\n"
                f"Если захочешь изменить время, просто напиши новое."
            )
        else:
            # Обновляем существующие настройки
            if "wakeup_time" in user_settings[user_id] and "sleep_time" in user_settings[user_id]:
                # Пользователь хочет изменить время
                user_settings[user_id]["wakeup_time"] = time_str
                sleep_time = user_settings[user_id]["sleep_time"]
                
                # Перепланируем уведомления
                schedule_user_notifications(user_id, time_str, sleep_time)
                save_users(user_settings)
                
                await message.answer(
                    f"Время пробуждения обновлено! 🌅\n\n"
                    f"Утро: {time_str}\n"
                    f"Вечер: {sleep_time}\n\n"
                    f"Настройки сохранены!"
                )
            else:
                # Что-то пошло не так, сбрасываем
                user_settings[user_id] = {"wakeup_time": time_str}
                await message.answer(
                    f"Утро: {time_str} 🌅\n\n"
                    f"А во сколько ты обычно ложишься спать? (например, 23:00)"
                )


@dp.message_handler()
async def handle_other_messages(message: types.Message):
    """Обработчик всех остальных сообщений"""
    await message.answer(
        "Я понимаю только время в формате ЧЧ:ММ (например, 07:30)\n\n"
        "Используй /start для начала настройки."
    )


async def on_startup(dp):
    """Функция запуска бота"""
    logger.info("Запуск бота...")
    
    # Загружаем настройки пользователей
    global user_settings
    user_settings = load_users()
    logger.info(f"Загружено настроек пользователей: {len(user_settings)}")
    
    # Планируем уведомления для всех пользователей
    for user_id, settings in user_settings.items():
        if "wakeup_time" in settings and "sleep_time" in settings:
            schedule_user_notifications(
                user_id, 
                settings["wakeup_time"], 
                settings["sleep_time"]
            )
    
    # Запускаем планировщик
    scheduler.start()
    logger.info("Планировщик запущен")


async def on_shutdown(dp):
    """Функция остановки бота"""
    logger.info("Остановка бота...")
    scheduler.shutdown()
    logger.info("Планировщик остановлен")


if __name__ == "__main__":
    # Запускаем бота
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)