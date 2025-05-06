# apps/ethikos/impact/urls.py

from django.urls import path
from ethikos.impact import views

app_name = "impact"

urlpatterns = [
    path('tracker/', views.tracker_list, name='impact-tracker-list'),
    path('tracker/<str:id>/', views.tracker_update, name='impact-tracker-update'),
    path('outcomes/', views.outcomes, name='impact-outcomes'),
    path('feedback/', views.feedback, name='impact-feedback'),
]
