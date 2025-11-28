from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet

router = DefaultRouter()
router.register(r'send', NotificationViewSet, basename='notification')

urlpatterns = [
    path('', include(router.urls)),
]