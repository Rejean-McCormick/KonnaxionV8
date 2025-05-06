# apps/kreative/artworks/admin.py

from django.contrib import admin
from kreative.artworks.models import Exhibition, Artwork
from django.utils.html import mark_safe

@admin.register(Exhibition)
class ExhibitionAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'location', 'created_at')
    list_filter = ('start_date', 'end_date')
    search_fields = ('name', 'description', 'location')
    ordering = ('-start_date',)
    
    fieldsets = (
        (None, {
            'fields': ('name', 'description')
        }),
        ('Détails de l\'exposition', {
            'fields': ('start_date', 'end_date', 'location')
        }),
    )

@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'exhibition', 'created_at', 'image_tag')
    list_filter = ('exhibition',)
    search_fields = ('title', 'description')
    ordering = ('title',)
    
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'exhibition')
        }),
        ('Image', {
            'fields': ('image',),
        }),
    )
    
    def image_tag(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" />')
        return ""
    image_tag.short_description = "Image"
