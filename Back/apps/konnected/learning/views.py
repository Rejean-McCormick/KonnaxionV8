from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAdminUser
from konnected.learning.models import Lesson, Quiz, Question, Answer
from konnected.learning.serializers import (
    LessonSerializer,
    QuizSerializer,
    QuestionSerializer,
    AnswerSerializer
)

class LessonViewSet(viewsets.ModelViewSet):
    """
    Gère les leçons interactives.
    Lecture pour tout utilisateur authentifié, écriture réservée aux admins.
    """
    serializer_class = LessonSerializer

    def get_queryset(self):
        return Lesson.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [IsAdminUser()]


class QuizViewSet(viewsets.ModelViewSet):
    """
    Gère les quiz associés aux leçons.
    Lecture pour tout utilisateur authentifié, écriture réservée aux admins.
    """
    serializer_class = QuizSerializer

    def get_queryset(self):
        return Quiz.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [IsAdminUser()]


class QuestionViewSet(viewsets.ModelViewSet):
    """
    Gère les questions des quiz.
    Lecture pour tout utilisateur authentifié, écriture réservée aux admins.
    """
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Question.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [IsAdminUser()]


class AnswerViewSet(viewsets.ModelViewSet):
    """
    Gère les réponses aux questions.
    Chaque réponse est liée à l'utilisateur connecté.
    """
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Answer.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
