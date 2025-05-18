"""
API Router for the Konnaxion Project

This file centralizes all API endpoints for the project. For simplicity, each
app exposes its endpoints in its own `urls.py` (instead of a separate `api/urls.py`).
"""

from django.urls import include, path

urlpatterns = [
    # Ekoh endpoints
    path(
        "api/ekoh/",
        include(("konnaxion.ekoh.urls", "ekoh"), namespace="ekoh"),
    ),

    # Debate Arena endpoints
    path(
        "api/debate/",
        include(("ethikos.debate_arena.urls", "debate_arena"), namespace="debate_arena"),
    ),

    # Ethikos suite of endpoints
    path(
        "api/ethikos/home/",
        include(("ethikos.home.urls", "home"), namespace="home"),
    ),
    path(
        "api/ethikos/knowledge-base/",
        include(("ethikos.knowledge_base.urls", "knowledge_base"), namespace="knowledge_base"),
    ),
    path(
        "api/ethikos/prioritization/",
        include(("ethikos.prioritization.urls", "prioritization"), namespace="prioritization"),
    ),
    path(
        "api/ethikos/resolution/",
        include(("ethikos.resolution.urls", "resolution"), namespace="resolution"),
    ),
    path(
        "api/ethikos/stats/",
        include(("ethikos.stats.urls", "stats"), namespace="stats"),
    ),

    # Additional Ethikos endpoints
    path(
        "api/impact/",
        include(("ethikos.impact.urls", "impact"), namespace="impact"),
    ),
    path(
        "api/learn/",
        include(("ethikos.learn.urls", "learn"), namespace="learn"),
    ),
    path(
        "api/pulse/",
        include(("ethikos.pulse.urls", "pulse"), namespace="pulse"),
    ),
    path(
        "api/trust/",
        include(("ethikos.trust.urls", "trust"), namespace="trust"),
    ),

    # Legacy "decide" mount for resolution
    path(
        "api/decide/",
        include(("ethikos.resolution.urls", "resolution"), namespace="decide"),
    ),

    # New alias: expose DebateTopicViewSet under /api/decide/topics/
    path(
        "api/decide/topics/",
        include(("ethikos.home.urls", "home")),
        name="decide-topics",
    ),

    # Deliberate endpoints
    path(
        "api/deliberate/",
        include(("ethikos.debate_arena.urls", "debate_arena"), namespace="deliberate"),
    ),

    # Keen apps endpoints
    path(
        "api/keen/collab-spaces/",
        include(("keenkonnect.collab_spaces.urls", "collab_spaces"), namespace="collab_spaces"),
    ),
    path(
        "api/keen/knowledge-hub/",
        include(("keenkonnect.knowledge_hub.urls", "knowledge_hub"), namespace="knowledge_hub"),
    ),
    path(
        "api/keen/projects/",
        include(("keenkonnect.projects.urls", "projects"), namespace="projects"),
    ),
    path(
        "api/keen/team-formation/",
        include(("keenkonnect.team_formation.urls", "team_formation"), namespace="team_formation"),
    ),

    # Konnaxion endpoints
    path(
        "api/konnaxion/core/",
        include(("konnaxion.core.urls", "core"), namespace="core"),
    ),
    path(
        "api/konnaxion/messaging/",
        include(("konnaxion.messaging.urls", "messaging"), namespace="messaging"),
    ),
    path(
        "api/konnaxion/notifications/",
        include(("konnaxion.notifications.urls", "notifications"), namespace="notifications"),
    ),
    path(
        "api/konnaxion/search/",
        include(("konnaxion.search.urls", "search"), namespace="search"),
    ),
    # The moderation module is currently commented out because it does not exist:
    # path("api/admin/", include(("konnaxion.moderation.urls", "moderation"), namespace="admin")),

    # Konnected endpoints
    path(
        "api/konnected/foundation/",
        include(("konnected.foundation.urls", "foundation"), namespace="foundation"),
    ),
    path(
        "api/konnected/konnectedcommunity/",
        include(("konnected.konnectedcommunity.urls", "community"), namespace="community"),
    ),
    path(
        "api/konnected/learning/",
        include(("konnected.learning.urls", "learning"), namespace="learning"),
    ),
    path(
        "api/konnected/offline/",
        include(("konnected.offline.urls", "offline"), namespace="offline"),
    ),

    # Kreative endpoints
    # path(
    #     "api/kreative/core/",
    #     include(("kreative.core.urls", "core"), namespace="core"),
    # ),

    # Add additional endpoints here as needed.
]
