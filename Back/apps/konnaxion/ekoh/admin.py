# apps/konnaxion/ekoh/admin.py

from django.contrib import admin
from konnaxion.ekoh.models import ExpertiseTag, ReputationProfile, ReputationEvent, WeightedVote

@admin.register(ExpertiseTag)
class ExpertiseTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(ReputationProfile)
class ReputationProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'reputation_score', 'ethical_multiplier', 'created_at')
    list_filter = ('user',)
    search_fields = ('user__username', 'user__email')
    ordering = ('-created_at',)

@admin.register(ReputationEvent)
class ReputationEventAdmin(admin.ModelAdmin):
    list_display = ('reputation_profile', 'event_type', 'event_value', 'timestamp')
    list_filter = ('event_type',)
    search_fields = ('reputation_profile__user__username',)
    ordering = ('-timestamp',)

@admin.register(WeightedVote)
class WeightedVoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'target_id', 'vote_value', 'weight', 'timestamp')
    search_fields = ('target_id',)
    ordering = ('-timestamp',)
