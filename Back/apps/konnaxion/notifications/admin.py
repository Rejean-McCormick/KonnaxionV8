# apps/konnaxion/notifications/admin.py

from django.contrib import admin
from konnaxion.notifications.models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read')
    search_fields = ('message',)
    ordering = ('-created_at',)
