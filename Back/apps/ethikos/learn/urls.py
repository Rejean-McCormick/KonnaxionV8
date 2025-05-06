# apps/ethikos/learn/urls.py

from django.urls import path
from ethikos.learn import views

app_name = "learn"

urlpatterns = [
    path('changelog/', views.changelog, name='learn-changelog'),
    path('guides/', views.guides, name='learn-guides'),
    path('glossary/', views.glossary, name='learn-glossary'),
]
