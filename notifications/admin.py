from django.contrib import admin
from .models import Notification, DeliveryLog, Recipient



class DeliveryLogInline(admin.TabularInline):
    model = DeliveryLog
    readonly_fields = ('channel', 'status', 'response_log', 'timestamp')
    can_delete = False
    extra = 0 # Не показывать пустые строки для добавления

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipient', 'status', 'sent_via', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('recipient__username', 'recipient__email')
    readonly_fields = ('status', 'sent_via')
    inlines = [DeliveryLogInline]

@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'telegram_id')