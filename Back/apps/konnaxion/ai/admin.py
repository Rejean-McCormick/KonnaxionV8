# apps/konnaxion/ai/admin.py

from django.contrib import admin
from konnaxion.ai.models import AIResult

@admin.register(AIResult)
class AIResultAdmin(admin.ModelAdmin):
    list_display = ('result_type', 'source_model', 'source_object_id', 'created_at')
    list_filter = ('result_type',)
    search_fields = ('source_model',)
    ordering = ('-created_at',)
