# apps/ethikos/knowledge_base/admin.py

from django.contrib import admin
from ethikos.knowledge_base.models import DebateArchive

@admin.register(DebateArchive)
class DebateArchiveAdmin(admin.ModelAdmin):
    list_display = ('title', 'debate_date', 'source', 'created_at')
    list_filter = ('debate_date',)
    search_fields = ('title', 'content')
    ordering = ('-debate_date',)
