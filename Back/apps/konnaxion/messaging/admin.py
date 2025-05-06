# apps/konnaxion/messaging/admin.py

from django.contrib import admin
from konnaxion.messaging.models import Conversation, Message

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_participants', 'created_at')
    search_fields = ('participants__username',)
    ordering = ('id',)

    def display_participants(self, obj):
        return ", ".join([user.username for user in obj.participants.all()])
    display_participants.short_description = "Participants"

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'sender', 'is_read', 'created_at')
    list_filter = ('is_read', 'sender')
    search_fields = ('content',)
    ordering = ('-created_at',)
