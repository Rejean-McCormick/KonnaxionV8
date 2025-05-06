# apps/konnaxion/urls.py

from django.urls import path, include

app_name = "konnaxion"

urlpatterns = [
    path(
        'core/',
        include(("konnaxion.core.urls", "core"), namespace="core"),
    ),
    path(
        'search/',
        include(("konnaxion.search.urls", "search"), namespace="search"),
    ),
    path(
        'ai/',
        include(("konnaxion.ai.urls", "ai"), namespace="ai"),
    ),
    path(
        'notifications/',
        include(("konnaxion.notifications.urls", "notifications"), namespace="notifications"),
    ),
    path(
        'messaging/',
        include(("konnaxion.messaging.urls", "messaging"), namespace="messaging"),
    ),
    path(
        'ekoh/',
        include(("konnaxion.ekoh.urls", "ekoh"), namespace="ekoh"),
    ),
]
