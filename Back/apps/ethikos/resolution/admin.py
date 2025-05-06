# apps/ethikos/resolution/admin.py

from django.contrib import admin
from ethikos.resolution.models import DebateResolution

@admin.register(DebateResolution)
class DebateResolutionAdmin(admin.ModelAdmin):
    list_display = ('debate_session', 'approved_by', 'approved_at', 'created_at')
    search_fields = ('debate_session__topic',)
    ordering = ('-approved_at',)
