# apps/keenkonnect/expert_match/admin.py

from django.contrib import admin
from keenkonnect.expert_match.models import ExpertMatchRequest, CandidateProfile, MatchScore

@admin.register(ExpertMatchRequest)
class ExpertMatchRequestAdmin(admin.ModelAdmin):
    list_display = ('project', 'requested_by', 'created_at')
    search_fields = ('project__title', 'requested_by__username')
    ordering = ('-created_at',)
    
    actions = ['trigger_matching']

    def trigger_matching(self, request, queryset):
        # Ici, vous pouvez intégrer un appel à une tâche asynchrone de matching
        count = queryset.count()
        self.message_user(request, f"Processus de matching déclenché pour {count} demande(s).")
    trigger_matching.short_description = "Déclencher le processus de matching pour les demandes sélectionnées"

@admin.register(CandidateProfile)
class CandidateProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'reputation_score', 'created_at')
    search_fields = ('user__username', 'user__email')
    ordering = ('-created_at',)

@admin.register(MatchScore)
class MatchScoreAdmin(admin.ModelAdmin):
    list_display = ('match_request', 'candidate', 'score', 'created_at')
    search_fields = ('match_request__project__title', 'candidate__user__username')
    ordering = ('-created_at',)
