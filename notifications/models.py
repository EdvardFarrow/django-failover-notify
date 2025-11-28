from django.db import models



def default_channels():
    return ['telegram', 'email', 'sms']



class Recipient(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    telegram_id = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return self.username
    
    
    
class Notification(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('sent', 'Отправлено'),
        ('failed', 'Не отправлено'),
    ]
    
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    status = models.CharField(choices=STATUS_CHOICES, default='pending', max_length=20)   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sent_via = models.CharField(max_length=20, null=True, blank=True)   
    channels_chain = models.JSONField(default=default_channels)
    
    def __str__(self):
        return f'Уведомление {self.id} для {self.recipient}'
    
    
    
class DeliveryLog(models.Model):
    """Лог попыток (чтобы видеть: Телеграм упал, СМС ушло)"""
    
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name="logs")
    channel = models.CharField(max_length=20)   # "Telegram", "email", "sms"
    status = models.CharField(max_length=20)    # "success", "failed"
    response_log = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)