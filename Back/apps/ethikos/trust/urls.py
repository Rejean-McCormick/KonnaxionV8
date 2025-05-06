# apps/ethikos/trust/urls.py

from django.urls import path
from ethikos.trust import views

app_name = "trust"

urlpatterns = [
    path('profile/', views.profile, name='trust-profile'),
    path('credentials/', views.credentials, name='trust-credentials'),
    path('badges/', views.badges, name='trust-badges'),
]
