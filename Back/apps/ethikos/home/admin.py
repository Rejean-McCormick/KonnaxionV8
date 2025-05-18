# apps/ethikos/home/admin.py

from django.contrib import admin
from ethikos.home.models import (
    DebateCategory,
    ResponseFormat,
    DebateTopic,
    FeaturedDebate,
    PersonalizedRecommendation,
    PublicVote,
)

@admin.register(DebateCategory)
class DebateCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_deleted')
    list_filter = ('is_deleted',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(ResponseFormat)
class ResponseFormatAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'is_deleted')
    list_filter = ('is_deleted',)
    search_fields = ('name', 'code')
    ordering = ('id',)

@admin.register(DebateTopic)
class DebateTopicAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'question',
        'debatecategory',
        'responseformat',
        'is_active',
        'is_deleted',
        'turnout',
        'created_at',
    )
    list_filter = ('debatecategory', 'responseformat', 'is_active', 'is_deleted')
    search_fields = ('question', 'description')
    ordering = ('question',)

@admin.register(FeaturedDebate)
class FeaturedDebateAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'debate_topic',
        'display_order',
        'active',
        'created_at',
    )
    list_filter = ('active',)
    search_fields = ('debate_topic__question',)
    ordering = ('display_order',)

@admin.register(PersonalizedRecommendation)
class PersonalizedRecommendationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'debate_topic',
        'score',
        'created_at',
    )
    list_filter = ('user',)
    search_fields = ('debate_topic__question',)
    ordering = ('-created_at',)

@admin.register(PublicVote)
class PublicVoteAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'topic',
        'value',
        'created_at',
    )
    list_filter = ('topic',)
    search_fields = ('value',)
    ordering = ('-created_at',)
