#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль для планирования уведомлений
"""

import asyncio
import logging
from datetime import datetime, time, timedelta
from typing import List, Callable
import threading
import time as time_module

logger = logging.getLogger(__name__)

class NotificationScheduler:
    def __init__(self):
        self.running = False
        self.thread = None
        self.bot_instance = None
        self.db = None
        
    def set_bot_instance(self, bot_instance):
        """Установить экземпляр бота для отправки уведомлений"""
        self.bot_instance = bot_instance
        self.db = bot_instance.db
    
    def start(self):
        """Запустить планировщик"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run_scheduler, daemon=True)
            self.thread.start()
            logger.info("Планировщик уведомлений запущен")
    
    def stop(self):
        """Остановить планировщик"""
        self.running = False
        if self.thread:
            self.thread.join()
        logger.info("Планировщик уведомлений остановлен")
    
    def _run_scheduler(self):
        """Основной цикл планировщика"""
        while self.running:
            try:
                current_time = datetime.now().time()
                
                # Проверяем утренние уведомления (8:00)
                if current_time.hour == 8 and current_time.minute == 0:
                    self._send_morning_notifications()
                
                # Проверяем вечерние уведомления (22:00)
                elif current_time.hour == 22 and current_time.minute == 0:
                    self._send_evening_notifications()
                
                # Ждём 1 минуту перед следующей проверкой
                time_module.sleep(60)
                
            except Exception as e:
                logger.error(f"Ошибка в планировщике: {e}")
                time_module.sleep(60)
    
    def _send_morning_notifications(self):
        """Отправить утренние уведомления"""
        if not self.bot_instance or not self.db:
            return
        
        try:
            # Получаем пользователей с включёнными утренними уведомлениями
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            user_ids = loop.run_until_complete(
                self.db.get_users_for_notification("morning")
            )
            
            logger.info(f"Отправка утренних уведомлений для {len(user_ids)} пользователей")
            
            for user_id in user_ids:
                try:
                    loop.run_until_complete(
                        self.bot_instance.send_scheduled_notification(user_id, "morning")
                    )
                except Exception as e:
                    logger.error(f"Ошибка отправки утреннего уведомления пользователю {user_id}: {e}")
            
            loop.close()
            
        except Exception as e:
            logger.error(f"Ошибка при отправке утренних уведомлений: {e}")
    
    def _send_evening_notifications(self):
        """Отправить вечерние уведомления"""
        if not self.bot_instance or not self.db:
            return
        
        try:
            # Получаем пользователей с включёнными вечерними уведомлениями
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            user_ids = loop.run_until_complete(
                self.db.get_users_for_notification("evening")
            )
            
            logger.info(f"Отправка вечерних уведомлений для {len(user_ids)} пользователей")
            
            for user_id in user_ids:
                try:
                    loop.run_until_complete(
                        self.bot_instance.send_scheduled_notification(user_id, "evening")
                    )
                except Exception as e:
                    logger.error(f"Ошибка отправки вечернего уведомления пользователю {user_id}: {e}")
            
            loop.close()
            
        except Exception as e:
            logger.error(f"Ошибка при отправке вечерних уведомлений: {e}")
    
    def schedule_custom_notification(self, user_id: int, notification_time: time, 
                                   notification_type: str, message: str):
        """Запланировать кастомное уведомление"""
        # Здесь можно добавить логику для планирования уведомлений в конкретное время
        # Пока что используем базовую логику с проверкой времени
        pass
    
    def cancel_notification(self, user_id: int, notification_type: str):
        """Отменить уведомление"""
        # Здесь можно добавить логику для отмены уведомлений
        pass