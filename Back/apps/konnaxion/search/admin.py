# apps/konnaxion/search/admin.py

from django.contrib import admin
from konnaxion.search.models import SearchIndex, SearchQueryLog

@admin.register(SearchIndex)
class SearchIndexAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_updated')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(SearchQueryLog)
class SearchQueryLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'query_text', 'results_count', 'created_at')
    list_filter = ('user',)
    search_fields = ('query_text',)
    ordering = ('-created_at',)
