# apps/konnected/team/admin.py

from django.contrib import admin
from konnected.team.models import Team, TeamInvitation

class TeamInvitationInline(admin.TabularInline):
    model = TeamInvitation
    extra = 0
    fields = ('invited_user', 'status', 'created_at')

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'member_count', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)
    inlines = [TeamInvitationInline]

    def member_count(self, obj):
        return obj.members.count()
    member_count.short_description = "Nombre de membres"

@admin.register(TeamInvitation)
class TeamInvitationAdmin(admin.ModelAdmin):
    list_display = ('team', 'invited_user', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('team__name', 'invited_user__username')
    ordering = ('-created_at',)
