# apps/konnected/paths/admin.py

from django.contrib import admin
from konnected.paths.models import LearningPath, PathStep

class PathStepInline(admin.TabularInline):
    model = PathStep
    extra = 1
    fields = ('knowledge_unit', 'order')

@admin.register(LearningPath)
class LearningPathAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('title',)
    inlines = [PathStepInline]

@admin.register(PathStep)
class PathStepAdmin(admin.ModelAdmin):
    list_display = ('learning_path', 'knowledge_unit', 'order')
    list_filter = ('learning_path',)
    ordering = ('learning_path', 'order')
