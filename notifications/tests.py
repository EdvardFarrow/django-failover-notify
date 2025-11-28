from django.test import TransactionTestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Recipient, Notification
from unittest.mock import patch

class NotificationApiTest(TransactionTestCase):
    
    reset_sequences = True
    
    def setUp(self):
        self.client = APIClient()
        self.recipient = Recipient.objects.create(
            username="TestUser",
            email="test@test.com"
        )
        self.url = '/api/send/'

    @patch('notifications.services.tasks.process_notification.delay')
    def test_create_notification_success(self, mock_task):
        data = {
            "recipient": self.recipient.id,
            "message": "Получилось",
            "channels_chain": ["email", "sms"]
        }
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.assertEqual(Notification.objects.count(), 1)
        
        mock_task.assert_called_once()

    def test_invalid_channel(self):
        data = {
            "recipient": self.recipient.id,
            "message": "Неудачно",
            "channels_chain": ["telepathy"] # Несуществующий канал
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)