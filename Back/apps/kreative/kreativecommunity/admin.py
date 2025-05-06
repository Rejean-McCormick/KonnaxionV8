# apps/kreative/community/admin.py

from django.contrib import admin
from kreative.kreativecommunity.models import CommunityPost, PostComment

@admin.register(CommunityPost)
class CommunityPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'posted_by', 'created_at')
    search_fields = ('title', 'content')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {'fields': ('title', 'content')}),
        ('Informations', {'fields': ('posted_by',)}),
    )

@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'commented_by', 'short_content', 'created_at')
    list_filter = ('post', 'commented_by')
    search_fields = ('content',)
    ordering = ('-created_at',)
    
    def short_content(self, obj):
        return (obj.content[:75] + '...') if len(obj.content) > 75 else obj.content
    short_content.short_description = "Contenu"
