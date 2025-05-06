# apps/ethikos/impact/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
def tracker_list(request):
    """
    GET /api/impact/tracker
    """
    data = {"items": []}
    return Response(data)

@api_view(['PATCH'])
def tracker_update(request, id):
    """
    PATCH /api/impact/tracker/{id}
    """
    # Here you would update the status of the tracker item with given id.
    # For now, just return no content.
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def outcomes(request):
    """
    GET /api/impact/outcomes
    """
    data = {"kpis": [], "charts": []}
    return Response(data)

@api_view(['GET','POST'])
def feedback(request):
    """
    GET /api/impact/feedback  - list feedback items
    POST /api/impact/feedback - submit new feedback
    """
    if request.method == 'GET':
        data = {"items": []}
        return Response(data)
    elif request.method == 'POST':
        # Here you would save the feedback from request.data
        return Response(status=status.HTTP_201_CREATED)
