# apps/konnaxion/ai/views.py

import logging

from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from konnaxion.ai.models import AIResult
from konnaxion.ai.serializers import AIResultSerializer
# Exemple : Importer la tâche d’analyse IA asynchrone
# from konnaxion.ai.tasks import generate_ai_result

logger = logging.getLogger(__name__)


class AIResultViewSet(viewsets.ModelViewSet):
    """
    Endpoints pour les résultats générés par l’IA.
    Possède une action personnalisée pour déclencher le traitement IA sur un objet source.
    """
    serializer_class = AIResultSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['source_model', 'source_object_id', 'status']  # à ajuster selon vos champs
    search_fields = ['result']                                         # à adapter si nécessaire
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = AIResult.objects.all()  # même logique que votre queryset initial
        logger.debug(
            "AIResult queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        instance = serializer.save()  # conserve votre logique de création
        logger.info(
            "AIResult créé (id=%s) via API par %s",
            instance.pk, self.request.user
        )
        return instance

    def perform_update(self, serializer):
        instance = serializer.save()
        logger.info(
            "AIResult mis à jour (id=%s) via API par %s",
            instance.pk, self.request.user
        )
        return instance

    def perform_destroy(self, instance):
        logger.info(
            "AIResult supprimé (id=%s) via API par %s",
            instance.pk, self.request.user
        )
        instance.delete()

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans AIResultViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)

    @action(detail=False, methods=['post'], url_path='generate', permission_classes=[permissions.IsAuthenticated])
    def generate(self, request):
        """
        Déclenche la génération d’un résultat IA pour un objet source.
        Expects 'source_model' et 'source_object_id' dans request.data.
        """
        source_model = request.data.get('source_model')
        source_object_id = request.data.get('source_object_id')
        if not source_model or not source_object_id:
            logger.warning(
                "generate manquant 'source_model' ou 'source_object_id' par %s",
                request.user
            )
            return Response(
                {"error": "Les champs 'source_model' et 'source_object_id' sont requis."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            # task = generate_ai_result.delay(source_model, source_object_id)
            logger.info(
                "Génération IA déclenchée pour source_model=%s, source_object_id=%s par %s",
                source_model, source_object_id, request.user
            )
            return Response(
                {
                    "message": "Génération IA déclenchée",
                    "source_model": source_model,
                    "source_object_id": source_object_id
                },
                status=status.HTTP_202_ACCEPTED
            )
        except Exception as exc:
            logger.exception(
                "Erreur lors de generate pour %s : %s",
                request.user, exc
            )
            return Response(
                {"detail": "Impossible de déclencher la génération IA."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
