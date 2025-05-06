# apps/ethikos/trust/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
def profile(request):
    """
    GET /api/trust/profile
    """
    data = {
        "avatar": None,
        "name": "Nom de l'utilisateur",
        "joined": "2025-01-01",
        "score": 0,
        "activity": []
    }
    return Response(data)

@api_view(['POST'])
def credentials(request):
    """
    POST /api/trust/credentials
    """
    # Here you would handle file upload from request.FILES
    return Response(status=status.HTTP_201_CREATED)

@api_view(['GET'])
def badges(request):
    """
    GET /api/trust/badges
    """
    data = {"earned": [], "progress": []}
    return Response(data)
