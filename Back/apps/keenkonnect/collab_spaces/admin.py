# apps/keenkonnect/collab_spaces/admin.py

from django.contrib import admin
from keenkonnect.collab_spaces.models import CollabSpace, Document, ChatMessage

@admin.register(CollabSpace)
class CollabSpaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'participant_count', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)
    
    def participant_count(self, obj):
        return obj.participants.count()
    participant_count.short_description = "Nombre de participants"

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'collab_space', 'uploaded_by', 'uploaded_at')
    list_filter = ('collab_space', 'uploaded_by')
    search_fields = ('title',)
    ordering = ('-uploaded_at',)

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('collab_space', 'sender', 'is_read', 'created_at')
    list_filter = ('is_read', 'sender')
    search_fields = ('message',)
    ordering = ('-created_at',)
    
    actions = ['mark_messages_as_read']

    def mark_messages_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f"{updated} message(s) marqué(s) comme lu(s).")
    mark_messages_as_read.short_description = "Marquer les messages sélectionnés comme lus"
