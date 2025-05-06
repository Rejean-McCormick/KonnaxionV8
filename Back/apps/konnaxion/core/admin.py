# apps/konnaxion/core/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from konnaxion.core.models import CustomUser, SystemConfiguration, ConfigurationChangeLog

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informations personnelles', {'fields': ('first_name', 'last_name', 'email', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    actions = ['activate_users', 'deactivate_users']

    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} utilisateur(s) activé(s).")
    activate_users.short_description = "Activer les utilisateurs sélectionnés"

    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} utilisateur(s) désactivé(s).")
    deactivate_users.short_description = "Désactiver les utilisateurs sélectionnés"


@admin.register(SystemConfiguration)
class SystemConfigurationAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'created_at')
    list_filter = ('key',)
    search_fields = ('key', 'value')
    ordering = ('key',)


@admin.register(ConfigurationChangeLog)
class ConfigurationChangeLogAdmin(admin.ModelAdmin):
    list_display = ('configuration', 'old_value', 'new_value', 'changed_by', 'created_at')
    list_filter = ('configuration', 'changed_by')
    search_fields = ('configuration__key',)
    ordering = ('-created_at',)
