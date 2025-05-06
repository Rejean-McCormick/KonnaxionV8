# apps/ethikos/debate_arena/admin.py

from django.contrib import admin
from ethikos.debate_arena.models import DebateSession, Argument, VoteRecord

@admin.register(DebateSession)
class DebateSessionAdmin(admin.ModelAdmin):
    list_display = ('topic', 'moderator', 'start_time', 'end_time', 'is_active', 'created_at')
    list_filter = ('is_active', 'moderator')
    search_fields = ('topic', 'description')
    ordering = ('-start_time',)
    
@admin.register(Argument)
class ArgumentAdmin(admin.ModelAdmin):
    list_display = ('short_content', 'debate_session', 'author', 'vote_count', 'created_at')
    list_filter = ('debate_session', 'author')
    search_fields = ('content',)
    ordering = ('-created_at',)

    def short_content(self, obj):
        return (obj.content[:75] + '...') if len(obj.content) > 75 else obj.content
    short_content.short_description = "Argument"

@admin.register(VoteRecord)
class VoteRecordAdmin(admin.ModelAdmin):
    list_display = ('argument', 'voter', 'vote_value', 'timestamp', 'created_at')
    list_filter = ('argument', 'voter')
    ordering = ('-timestamp',)
