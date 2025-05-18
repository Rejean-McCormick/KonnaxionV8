# apps/konnected/learning/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from konnected.learning.views import (
    LessonViewSet,
    QuizViewSet,
    QuestionViewSet,
    AnswerViewSet,
)

app_name = "learning"

router = DefaultRouter()
router.register(r"lessons", LessonViewSet, basename="lessons")
router.register(r"quizzes", QuizViewSet, basename="quizzes")
router.register(r"questions", QuestionViewSet, basename="questions")
router.register(r"answers", AnswerViewSet, basename="answers")

urlpatterns = [
    path("", include((router.urls, app_name), namespace=app_name)),
]
