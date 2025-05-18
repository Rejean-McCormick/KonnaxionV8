# apps/debug/views.py

import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

logger = logging.getLogger(__name__)

class DebugTestView(APIView):
    """
    Endpoint de test de debug.
    Accessible uniquement aux utilisateurs staff ou superusers.
    """
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        logger.debug("Accès à DebugTestView par %s", request.user)
        # Message conservé à l’identique
        return Response({"message": "Debug test is working!"})

    def handle_exception(self, exc):
        logger.exception("Erreur dans DebugTestView pour %s : %s", request.user, exc)
        return super().handle_exception(exc)

from django.http import HttpResponse

def debug_test(request):
    return HttpResponse("Debug test OK")
