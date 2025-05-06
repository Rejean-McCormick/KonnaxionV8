# konnaxion_project/config/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from konnaxion.views import debug_test 

# Import API URLs from your custom router
from .api_router import urlpatterns as api_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(api_urlpatterns)),  # URLs from api_router.py (no version prefix)
    path('konnaxion/', include('konnaxion.urls')),
    path('keenkonnect/', include('keenkonnect.urls')),
    path('ethikos/', include('ethikos.urls')),
    path('kreative/', include('kreative.urls')),
    path("debug-test/", debug_test, name="debug-test"),
    path('api-auth/', include('rest_framework.urls')),
]

# Include URLs for the sub-applications contained in the "konnected" folder
konnected_patterns = [
    path('foundation/', include('konnected.foundation.urls')),
    path('konnectedcommunity/', include('konnected.konnectedcommunity.urls')),
    path('learning/', include('konnected.learning.urls')),
    path('offline/', include('konnected.offline.urls')),
    path('paths/', include('konnected.paths.urls')),
    path('team/', include('konnected.team.urls')),
]

urlpatterns += [
    path('konnected/', include((konnected_patterns, 'konnected'), namespace='konnected')),
]

# Add Django Debug Toolbar URLs only in development mode
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
