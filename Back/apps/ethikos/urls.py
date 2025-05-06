# apps/ethikos/urls.py

from django.urls import path, include

app_name = "ethikos"

urlpatterns = [
    path(
        'home/',
        include(('ethikos.home.urls', 'home'), namespace='home'),
    ),
    path(
        'debate_arena/',
        include(('ethikos.debate_arena.urls', 'debate_arena'), namespace='debate_arena'),
    ),
    path(
        'stats/',
        include(('ethikos.stats.urls', 'stats'), namespace='stats'),
    ),
    path(
        'knowledge_base/',
        include(('ethikos.knowledge_base.urls', 'knowledge_base'), namespace='knowledge_base'),
    ),
    path(
        'prioritization/',
        include(('ethikos.prioritization.urls', 'prioritization'), namespace='prioritization'),
    ),
    path(
        'resolution/',
        include(('ethikos.resolution.urls', 'resolution'), namespace='resolution'),
    ),
]
