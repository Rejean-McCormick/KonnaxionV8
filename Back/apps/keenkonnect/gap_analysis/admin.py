# apps/keenkonnect/gap_analysis/admin.py

from django.contrib import admin
from keenkonnect.gap_analysis.models import GapAnalysis

@admin.register(GapAnalysis)
class GapAnalysisAdmin(admin.ModelAdmin):
    list_display = ('project', 'planned_progress', 'actual_progress', 'gap', 'created_at')
    list_filter = ('project__status',)  # Si le projet possède un champ "status"
    search_fields = ('project__title',)
    ordering = ('-created_at',)
