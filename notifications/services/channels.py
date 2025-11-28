from abc import ABC, abstractmethod
import random
import time

class BaseChannel(ABC):
    @abstractmethod
    def send(self, user: str, message: str) -> bool:
        pass



class EmailChannel(BaseChannel):
    def send(self, recipient: str, message: str) -> bool:
        
        print(f"Попытка отправки Email для {recipient.username}...")
        
        if not recipient.email:
            raise ValueError("Нет email для отправки")
        
        # Эмуляция: 30% шанс падения сервиса (показать Failover)
        if random.random() < 0.3:
            print("Ошибка: SMTP сервер недоступен")
            raise ConnectionError("SMTP Timeout")
            
        print(f"[Email отправлен] Адрес: {recipient.email} | Текст: {message}")
        return True



class TelegramChannel(BaseChannel):
    def send(self, recipient: str, message: str) -> bool:
        
        print(f"Попытка отправки в Telegram для {recipient.username}...")
        
        if not recipient.telegram_id:
            raise ValueError(f"У пользователя {recipient.username} нет Telegram ID")
        
        if random.random() < 0.5:
            print("Ошибка: Telegram API не отвечает (Timeout)")
            raise ConnectionError("Telegram API Timeout")

        print(f"[Telegram отправлен] ID: {recipient.telegram_id} | Текст: {message}")
        return True
    
    
class SMSChannel(BaseChannel):
    def send(self, recipient: str, message: str) -> bool:
        
        print(f"Попытка отправки SMS для {recipient.username}...")
        
        if not recipient.phone:
            raise ValueError("Нет телефона")

        # SMS считаем самым надежным, без рандомных ошибок
        print(f"[SMS отправлено] Телефон: {recipient.phone} | Текст: {message}")
        return True