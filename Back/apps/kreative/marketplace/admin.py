# apps/kreative/marketplace/admin.py

from django.contrib import admin
from kreative.marketplace.models import ArtistProfile, Commission, MarketplaceListing

@admin.register(ArtistProfile)
class ArtistProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'portfolio_url', 'created_at')
    search_fields = ('user__username', 'portfolio_url')
    ordering = ('-created_at',)

@admin.register(Commission)
class CommissionAdmin(admin.ModelAdmin):
    list_display = ('title', 'requested_by', 'status', 'budget', 'created_at')
    list_filter = ('status', 'requested_by')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    
    actions = ['change_status']
    
    def change_status(self, request, queryset):
        new_status = request.POST.get('new_status')
        if new_status:
            updated = queryset.update(status=new_status)
            self.message_user(request, f"{updated} commission(s) mise(s) à jour avec le statut {new_status}.")
        else:
            self.message_user(request, "Veuillez spécifier un nouveau statut.", level='error')
    change_status.short_description = "Changer le statut des commissions sélectionnées"

@admin.register(MarketplaceListing)
class MarketplaceListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist_profile', 'price', 'status', 'created_at')
    list_filter = ('status', 'artist_profile')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
