# apps/ethikos/learn/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def changelog(request):
    """
    GET /api/learn/changelog
    """
    data = {"entries": []}
    return Response(data)

@api_view(['GET'])
def guides(request):
    """
    GET /api/learn/guides
    """
    data = {"sections": []}
    return Response(data)

@api_view(['GET'])
def glossary(request):
    """
    GET /api/learn/glossary
    """
    data = {"items": []}
    return Response(data)
