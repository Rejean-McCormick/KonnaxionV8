# apps/kreative/immersive/admin.py

from django.contrib import admin
from kreative.immersive.models import ImmersiveExperience

@admin.register(ImmersiveExperience)
class ImmersiveExperienceAdmin(admin.ModelAdmin):
    list_display = ('title', 'media_url', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {'fields': ('title', 'description')}),
        ('Contenu Immersif', {'fields': ('media_url',)}),
    )
