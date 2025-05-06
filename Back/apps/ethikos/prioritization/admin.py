# apps/ethikos/prioritization/admin.py

from django.contrib import admin
from ethikos.prioritization.models import DebatePrioritization

@admin.register(DebatePrioritization)
class DebatePrioritizationAdmin(admin.ModelAdmin):
    list_display = ('debate_session', 'ranking_score', 'created_at')
    list_filter = ('debate_session',)
    ordering = ('-created_at',)
