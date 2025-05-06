# apps/konnected/konnectedcommunity/admin.py

from django.contrib import admin
from konnected.konnectedcommunity.models import DiscussionThread, Comment

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    fields = ('author', 'content', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(DiscussionThread)
class DiscussionThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'comment_count')
    search_fields = ('title', 'content')
    ordering = ('-created_at',)
    inlines = [CommentInline]

    def comment_count(self, obj):
        return obj.comments.count()
    comment_count.short_description = "Nombre de commentaires"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('thread', 'author', 'short_content', 'created_at')
    list_filter = ('thread', 'author')
    search_fields = ('content',)
    ordering = ('-created_at',)

    def short_content(self, obj):
        return (obj.content[:75] + '...') if len(obj.content) > 75 else obj.content
    short_content.short_description = "Contenu"
