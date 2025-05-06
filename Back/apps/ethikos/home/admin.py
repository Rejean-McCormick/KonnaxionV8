# apps/ethikos/home/admin.py

from django.contrib import admin
from ethikos.home.models import DebateTopic, FeaturedDebate, PersonalizedRecommendation

@admin.register(DebateTopic)
class DebateTopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'publish_date', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    ordering = ('title',)

@admin.register(FeaturedDebate)
class FeaturedDebateAdmin(admin.ModelAdmin):
    list_display = ('debate_topic', 'display_order', 'active', 'created_at')
    list_filter = ('active',)
    ordering = ('display_order',)

@admin.register(PersonalizedRecommendation)
class PersonalizedRecommendationAdmin(admin.ModelAdmin):
    list_display = ('user', 'debate_topic', 'score', 'created_at')
    list_filter = ('user',)
    search_fields = ('debate_topic__title',)
    ordering = ('-created_at',)
