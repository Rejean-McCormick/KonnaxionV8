# apps/keenkonnect/team_formation/admin.py

from django.contrib import admin
from keenkonnect.team_formation.models import TeamFormationRequest, TeamFormationCandidate

@admin.register(TeamFormationRequest)
class TeamFormationRequestAdmin(admin.ModelAdmin):
    list_display = ('project', 'requested_by', 'created_at')
    search_fields = ('project__title', 'requested_by__username')
    ordering = ('-created_at',)
    
    actions = ['trigger_team_formation']

    def trigger_team_formation(self, request, queryset):
        # Intégrer ici l'appel à une tâche asynchrone si besoin
        count = queryset.count()
        self.message_user(request, f"Processus de formation d'équipe déclenché pour {count} demande(s).")
    trigger_team_formation.short_description = "Déclencher la formation d'équipe pour les demandes sélectionnées"

@admin.register(TeamFormationCandidate)
class TeamFormationCandidateAdmin(admin.ModelAdmin):
    list_display = ('formation_request', 'user', 'compatibility_score', 'created_at')
    search_fields = ('user__username',)
    ordering = ('-created_at',)
