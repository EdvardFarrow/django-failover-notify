from celery import shared_task
from django.db import transaction
from ..models import Notification, DeliveryLog
from .channels import EmailChannel, SMSChannel, TelegramChannel



CHANNEL_MAP = {
    'email': EmailChannel,
    'sms': SMSChannel,
    'telegram': TelegramChannel,
}


@shared_task(bind=True)
def process_notification(self, notification_id):
    
    try:
        notification = Notification.objects.get(id=notification_id)
    except Notification.DoesNotExist:
        return "Уведомление не найдено"

    chain = notification.channels_chain or ['telegram', 'email', 'sms']
    
    for channel_name in chain:
        sender_cls = CHANNEL_MAP.get(channel_name)
        if not sender_cls:
            continue
            
        sender = sender_cls()
        
        try:
            # Вызываем метод отправки
            sender.send(notification.recipient, notification.message)
            
            with transaction.atomic():
                DeliveryLog.objects.create(
                    notification=notification,
                    channel=channel_name,
                    status='success',
                    response_log="OK"
                )
                notification.status = 'sent'
                notification.sent_via = channel_name
                notification.save()
            
            return f"Отправлено через {channel_name}"
            
        except Exception as e:
            # Логируем неудачу и идем дальше
            with transaction.atomic():
                DeliveryLog.objects.create(
                    notification=notification,
                    channel=channel_name,
                    status='failed',
                    response_log=str(e)
                )
            # continue (он тут неявный, цикл идет дальше)

    # Если цикл кончился
    notification.status = 'failed'
    notification.save()
    return "All channels failed"