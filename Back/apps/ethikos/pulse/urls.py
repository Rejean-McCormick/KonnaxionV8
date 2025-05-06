# apps/ethikos/pulse/urls.py

from django.urls import path
from ethikos.pulse import views

app_name = "pulse"

urlpatterns = [
    path('overview/', views.overview, name='pulse-overview'),
    path('live/', views.live_metrics, name='pulse-live'),
    path('trends/', views.trends, name='pulse-trends'),
    path('health/', views.health, name='pulse-health'),
]
