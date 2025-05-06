from django.contrib import admin

class BaseAdmin(admin.ModelAdmin):
    """
    A base ModelAdmin with common configurations such as readonly fields,
    list filters, and search fields.
    """
    readonly_fields = ('created_at', 'updated_at',)
    list_filter = ('created_at', 'updated_at',)
    search_fields = ('id',)
