# apps/keenkonnect/urls.py

from django.urls import path, include

app_name = "keenkonnect"

urlpatterns = [
    path(
        'projects/',
        include(('keenkonnect.projects.urls', 'projects'), namespace='projects'),
    ),
    path(
        'gap_analysis/',
        include(('keenkonnect.gap_analysis.urls', 'gap_analysis'), namespace='gap_analysis'),
    ),
    path(
        'expert_match/',
        include(('keenkonnect.expert_match.urls', 'expert_match'), namespace='expert_match'),
    ),
    path(
        'team_formation/',
        include(('keenkonnect.team_formation.urls', 'team_formation'), namespace='team_formation'),
    ),
    path(
        'collab_spaces/',
        include(('keenkonnect.collab_spaces.urls', 'collab_spaces'), namespace='collab_spaces'),
    ),
    path(
        'knowledge_hub/',
        include(('keenkonnect.knowledge_hub.urls', 'knowledge_hub'), namespace='knowledge_hub'),
    ),
]
