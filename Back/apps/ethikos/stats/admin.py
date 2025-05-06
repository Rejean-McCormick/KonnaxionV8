# apps/ethikos/stats/admin.py

from django.contrib import admin
from ethikos.stats.models import DebateStatistic, DebateEventLog

@admin.register(DebateStatistic)
class DebateStatisticAdmin(admin.ModelAdmin):
    list_display = ('debate_session', 'metric_name', 'value', 'recorded_at')
    list_filter = ('debate_session', 'metric_name')
    ordering = ('-recorded_at',)

@admin.register(DebateEventLog)
class DebateEventLogAdmin(admin.ModelAdmin):
    list_display = ('debate_session', 'event_type', 'timestamp')
    list_filter = ('debate_session', 'event_type')
    ordering = ('-timestamp',)
