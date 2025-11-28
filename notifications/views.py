from rest_framework import viewsets
from django.db import transaction
from .serializers import NotificationSerializer
from .models import Notification
from .services.tasks import process_notification

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        transaction.on_commit(lambda: process_notification.delay(instance.id))