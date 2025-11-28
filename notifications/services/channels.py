from abc import ABC, abstractmethod
import random
from typing import Any
import logging

logger = logging.getLogger(__name__)



class BaseChannel(ABC):
    @abstractmethod
    def send(self, recipient: Any, message: str) -> bool:
        pass



class EmailChannel(BaseChannel):
    def send(self, recipient: Any, message: str) -> bool:
        
        logger.info(f"Попытка отправки Email для {recipient.username}...")
        
        if not recipient.email:
            logger.warning(f"У пользователя {recipient.username} нет email")
            raise ValueError("Нет email для отправки")
        
        # Эмуляция: 30% шанс падения сервиса (показать Failover)
        if random.random() < 0.3:
            logger.error("Ошибка: SMTP сервер недоступен")
            raise ConnectionError("SMTP Timeout")
            
        logger.info(f"[Email отправлен] Адрес: {recipient.email} | Текст: {message}")
        return True



class TelegramChannel(BaseChannel):
    def send(self, recipient: Any, message: str) -> bool:
        
        logger.info(f"Попытка отправки в Telegram для {recipient.username}...")
        
        if not recipient.telegram_id:
            logger.warning(f"У пользователя {recipient.username} нет Telegram ID")
            raise ValueError("Не указан Telegram ID")
        
        if random.random() < 0.5:
            logger.error("Ошибка: Telegram API не отвечает (Timeout)")
            raise ConnectionError("Telegram API Timeout")

        logger.info(f"[Telegram отправлен] ID: {recipient.telegram_id} | Текст: {message}")
        return True
    
    
class SMSChannel(BaseChannel):
    def send(self, recipient: Any, message: str) -> bool:
        
        logger.info(f"Попытка отправки SMS для {recipient.username}...")
        
        if not recipient.phone:
            logger.warning(f"У пользователя {recipient.username} не указан телефон")
            raise ValueError("Нет телефона")

        # SMS считаем самым надежным, без рандомных ошибок
        logger.info(f"[SMS отправлено] Телефон: {recipient.phone} | Текст: {message}")
        return True