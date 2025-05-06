# apps/ethikos/pulse/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def overview(request):
    """
    GET /api/pulse/overview
    """
    data = {"refreshedAt": "", "kpis": []}
    return Response(data)

@api_view(['GET'])
def live_metrics(request):
    """
    GET /api/pulse/live
    """
    data = {"counters": []}
    return Response(data)

@api_view(['GET'])
def trends(request):
    """
    GET /api/pulse/trends
    """
    data = {"charts": []}
    return Response(data)

@api_view(['GET'])
def health(request):
    """
    GET /api/pulse/health
    """
    data = {"radarConfig": {}, "pieConfig": {}}
    return Response(data)
