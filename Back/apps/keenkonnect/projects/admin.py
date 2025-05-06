# apps/keenkonnect/projects/admin.py

from django.contrib import admin
from keenkonnect.projects.models import Project, Milestone, Task

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'progress', 'status', 'start_date', 'end_date', 'created_at')
    list_filter = ('status', 'owner')
    search_fields = ('title', 'description')
    ordering = ('title',)
    
    actions = ['mark_as_completed']

    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f"{updated} projet(s) marqué(s) comme terminé(s).")
    mark_as_completed.short_description = "Marquer les projets sélectionnés comme terminés"

@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'due_date', 'status', 'created_at')
    list_filter = ('project', 'status')
    search_fields = ('title',)
    ordering = ('project', 'due_date')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'milestone', 'assigned_to', 'is_completed', 'created_at')
    list_filter = ('milestone', 'is_completed')
    search_fields = ('title', 'description')
    ordering = ('milestone', 'title')
    
    actions = ['mark_tasks_completed']

    def mark_tasks_completed(self, request, queryset):
        updated = queryset.update(is_completed=True)
        self.message_user(request, f"{updated} tâche(s) marquée(s) comme complétée(s).")
    mark_tasks_completed.short_description = "Marquer les tâches sélectionnées comme complétées"
