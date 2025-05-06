# apps/konnected/foundation/admin.py

from django.contrib import admin
from konnected.foundation.models import KnowledgeUnit

@admin.register(KnowledgeUnit)
class KnowledgeUnitAdmin(admin.ModelAdmin):
    list_display = ('title', 'language', 'version', 'created_at')
    list_filter = ('language', 'version')
    search_fields = ('title', 'content')
    ordering = ('title',)
    
    fieldsets = (
        (None, {'fields': ('title', 'content')}),
        ('Détails', {'fields': ('language', 'version')}),
    )
