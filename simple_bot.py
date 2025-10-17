#!/usr/bin/env python3
"""
Простой Telegram-бот Warmly без сложных зависимостей
Использует только стандартную библиотеку Python и requests
"""

import json
import os
import time
import random
import logging
from datetime import datetime
from typing import Dict, Any
import requests
from threading import Thread
import schedule
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

# URL для API Telegram
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

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
    phrase_list = phrases.get(phrase_type, [])
    return random.choice(phrase_list) if phrase_list else "Хорошего дня! 🌟"


def send_message(chat_id: str, text: str) -> bool:
    """Отправляет сообщение пользователю"""
    try:
        url = f"{API_URL}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML"
        }
        response = requests.post(url, data=data, timeout=10)
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения: {e}")
        return False


def send_morning_message(user_id: str):
    """Отправляет утреннее сообщение пользователю"""
    phrase = get_random_phrase("morning")
    if send_message(user_id, phrase):
        logger.info(f"Утреннее сообщение отправлено пользователю {user_id}")
    else:
        logger.error(f"Ошибка при отправке утреннего сообщения пользователю {user_id}")


def send_evening_message(user_id: str):
    """Отправляет вечернее сообщение пользователю"""
    phrase = get_random_phrase("evening")
    if send_message(user_id, phrase):
        logger.info(f"Вечернее сообщение отправлено пользователю {user_id}")
    else:
        logger.error(f"Ошибка при отправке вечернего сообщения пользователю {user_id}")


def schedule_user_notifications(user_id: str, wakeup_time: str, sleep_time: str):
    """Планирует уведомления для пользователя"""
    # Удаляем старые задачи для этого пользователя
    schedule.clear(f"morning_{user_id}")
    schedule.clear(f"evening_{user_id}")
    
    # Планируем утренние уведомления
    schedule.every().day.at(wakeup_time).do(send_morning_message, user_id).tag(f"morning_{user_id}")
    
    # Планируем вечерние уведомления
    schedule.every().day.at(sleep_time).do(send_evening_message, user_id).tag(f"evening_{user_id}")
    
    logger.info(f"Уведомления запланированы для пользователя {user_id}: утро {wakeup_time}, вечер {sleep_time}")


def get_updates(offset: int = 0) -> list:
    """Получает обновления от Telegram"""
    try:
        url = f"{API_URL}/getUpdates"
        params = {"offset": offset, "timeout": 30}
        response = requests.get(url, params=params, timeout=35)
        if response.status_code == 200:
            data = response.json()
            return data.get("result", [])
        return []
    except Exception as e:
        logger.error(f"Ошибка при получении обновлений: {e}")
        return []


def process_message(update: dict):
    """Обрабатывает входящее сообщение"""
    message = update.get("message", {})
    if not message:
        return
    
    user_id = str(message["from"]["id"])
    text = message.get("text", "")
    
    if text == "/start":
        if user_id in user_settings:
            # Пользователь уже настроен
            settings = user_settings[user_id]
            wakeup = settings.get("wakeup_time", "не установлено")
            sleep = settings.get("sleep_time", "не установлено")
            
            send_message(user_id, 
                f"Привет! 🌿\n\n"
                f"Ты уже настроен!\n"
                f"Утро: {wakeup} | Вечер: {sleep}\n\n"
                f"Просто напиши новое время, чтобы изменить.\n"
                f"Формат: ЧЧ:ММ (например, 07:30)"
            )
        else:
            # Новый пользователь
            send_message(user_id,
                "Привет! 🌿\n\n"
                "Я Warmly — твой ежедневный помощник для эмоциональной поддержки.\n"
                "Я буду присылать тебе тёплые фразы утром и вечером.\n\n"
                "Давай настроим твоё расписание!\n\n"
                "Во сколько ты обычно просыпаешься? (например, 07:00)"
            )
    
    elif text and text.count(':') == 1 and len(text.split(':')) == 2:
        # Обработка времени
        if not validate_time(text):
            send_message(user_id, "Неверный формат времени! Используй ЧЧ:ММ (например, 07:30)")
            return
        
        if user_id not in user_settings:
            # Первый раз - запрашиваем время пробуждения
            user_settings[user_id] = {"wakeup_time": text}
            send_message(user_id,
                f"Отлично! Утро: {text} 🌅\n\n"
                f"А во сколько ты обычно ложишься спать? (например, 23:00)"
            )
        else:
            # Обновляем настройки
            if "wakeup_time" in user_settings[user_id] and "sleep_time" not in user_settings[user_id]:
                # Устанавливаем время сна
                user_settings[user_id]["sleep_time"] = text
                wakeup = user_settings[user_id]["wakeup_time"]
                
                # Планируем уведомления
                schedule_user_notifications(user_id, wakeup, text)
                
                # Сохраняем в файл
                save_users(user_settings)
                
                send_message(user_id,
                    f"Отлично! Настройки сохранены! 🌿\n\n"
                    f"Утро: {wakeup} 🌅\n"
                    f"Вечер: {text} 🌙\n\n"
                    f"Я буду присылать тебе тёплые фразы в это время каждый день!\n"
                    f"Если захочешь изменить время, просто напиши новое."
                )
            else:
                # Обновляем существующие настройки
                if "wakeup_time" in user_settings[user_id] and "sleep_time" in user_settings[user_id]:
                    # Пользователь хочет изменить время
                    user_settings[user_id]["wakeup_time"] = text
                    sleep_time = user_settings[user_id]["sleep_time"]
                    
                    # Перепланируем уведомления
                    schedule_user_notifications(user_id, text, sleep_time)
                    save_users(user_settings)
                    
                    send_message(user_id,
                        f"Время пробуждения обновлено! 🌅\n\n"
                        f"Утро: {text}\n"
                        f"Вечер: {sleep_time}\n\n"
                        f"Настройки сохранены!"
                    )
                else:
                    # Что-то пошло не так, сбрасываем
                    user_settings[user_id] = {"wakeup_time": text}
                    send_message(user_id,
                        f"Утро: {text} 🌅\n\n"
                        f"А во сколько ты обычно ложишься спать? (например, 23:00)"
                    )
    
    else:
        # Неизвестное сообщение
        send_message(user_id,
            "Я понимаю только время в формате ЧЧ:ММ (например, 07:30)\n\n"
            "Используй /start для начала настройки."
        )


def scheduler_worker():
    """Рабочий поток для планировщика"""
    while True:
        schedule.run_pending()
        time.sleep(1)


def main():
    """Главная функция"""
    global phrases, user_settings
    
    logger.info("Запуск бота...")
    
    # Загружаем фразы
    with open(PHRASES_FILE, "r", encoding="utf-8") as f:
        phrases = json.load(f)
    
    # Загружаем настройки пользователей
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
    
    # Запускаем планировщик в отдельном потоке
    scheduler_thread = Thread(target=scheduler_worker, daemon=True)
    scheduler_thread.start()
    logger.info("Планировщик запущен")
    
    # Основной цикл получения сообщений
    offset = 0
    while True:
        try:
            updates = get_updates(offset)
            for update in updates:
                process_message(update)
                offset = update["update_id"] + 1
        except KeyboardInterrupt:
            logger.info("Остановка бота...")
            break
        except Exception as e:
            logger.error(f"Ошибка в основном цикле: {e}")
            time.sleep(5)


if __name__ == "__main__":
    main()