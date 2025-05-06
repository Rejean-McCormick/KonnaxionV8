# apps/konnected/offline/admin.py

from django.contrib import admin
from django.contrib import messages
from konnected.offline.models import OfflineContentPackage

@admin.register(OfflineContentPackage)
class OfflineContentPackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'last_synced', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    
    actions = ['trigger_sync']

    def trigger_sync(self, request, queryset):
        # Ici, vous pouvez intégrer l'appel à une tâche asynchrone par exemple via Celery.
        # Pour l'instant, nous simulons simplement l'action avec un message.
        count = queryset.count()
        # Exemple d'appel : sync_offline_content.delay(package.id) pour chaque package
        self.message_user(request, f"Sync déclenché pour {count} package(s).", messages.SUCCESS)
    trigger_sync.short_description = "Déclencher la synchronisation des packages offline"
