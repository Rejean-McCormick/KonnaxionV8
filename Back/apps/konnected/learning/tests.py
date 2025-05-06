# apps/konnected/learning/tests.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from konnected.learning.models import Lesson, Quiz, Question, Answer

User = get_user_model()

# ------------------------------------------------------------------------------
# 1. Tests Unitaires des Modèles (Model Tests)
# ------------------------------------------------------------------------------

class LessonModelTests(TestCase):
    def test_create_lesson(self):
        """
        Teste la création d'une instance de Lesson.
        Vérifie que le titre et le contenu sont correctement enregistrés et que
        la méthode __str__ retourne bien le titre.
        """
        lesson = Lesson.objects.create(
            title="Introduction aux tests",
            content="Ce cours explique comment écrire des tests unitaires."
        )
        self.assertEqual(lesson.title, "Introduction aux tests")
        self.assertEqual(lesson.content, "Ce cours explique comment écrire des tests unitaires.")
        self.assertEqual(str(lesson), "Introduction aux tests")


class QuizModelTests(TestCase):
    def setUp(self):
        self.lesson = Lesson.objects.create(
            title="Leçon pour Quiz",
            content="Contenu de la leçon pour tester un quiz."
        )

    def test_create_quiz(self):
        """
        Teste la création d'un quiz associé à une leçon.
        Vérifie que le titre, les instructions et la durée sont correctement enregistrés.
        """
        quiz = Quiz.objects.create(
            lesson=self.lesson,
            title="Quiz de Test",
            instructions="Répondez correctement aux questions.",
            time_limit=30
        )
        self.assertEqual(quiz.title, "Quiz de Test")
        self.assertEqual(quiz.instructions, "Répondez correctement aux questions.")
        self.assertEqual(quiz.time_limit, 30)
        self.assertEqual(quiz.lesson, self.lesson)


class QuestionModelTests(TestCase):
    def setUp(self):
        self.lesson = Lesson.objects.create(
            title="Leçon pour Question",
            content="Contenu pour tester les questions."
        )
        self.quiz = Quiz.objects.create(
            lesson=self.lesson,
            title="Quiz de Question",
            instructions="Veuillez répondre aux questions.",
            time_limit=20
        )

    def test_create_question(self):
        """
        Teste la création d'une question pour un quiz.
        Vérifie que le texte, le type de question et la réponse correcte sont enregistrés.
        """
        question = Question.objects.create(
            quiz=self.quiz,
            text="Qu'est-ce qu'un test unitaire ?",
            question_type="text",
            correct_answer="Un test sur une unité de code."
        )
        self.assertEqual(question.text, "Qu'est-ce qu'un test unitaire ?")
        self.assertEqual(question.question_type, "text")
        self.assertEqual(question.correct_answer, "Un test sur une unité de code.")
        self.assertEqual(question.quiz, self.quiz)


class AnswerModelTests(TestCase):
    def setUp(self):
        self.lesson = Lesson.objects.create(
            title="Leçon pour Réponse",
            content="Contenu pour tester les réponses."
        )
        self.quiz = Quiz.objects.create(
            lesson=self.lesson,
            title="Quiz de Réponse",
            instructions="Sélectionnez la bonne réponse.",
            time_limit=15
        )
        self.question = Question.objects.create(
            quiz=self.quiz,
            text="Que signifie API ?",
            question_type="multiple_choice",
            correct_answer="Interface de Programmation d'Application"
        )

    def test_create_answer(self):
        """
        Teste la création d'une réponse pour une question.
        Vérifie que le texte et le statut de correction sont correctement enregistrés.
        """
        answer = Answer.objects.create(
            question=self.question,
            text="Interface de Programmation d'Application",
            is_correct=True
        )
        self.assertEqual(answer.text, "Interface de Programmation d'Application")
        self.assertTrue(answer.is_correct)
        self.assertEqual(answer.question, self.question)

# ------------------------------------------------------------------------------
# 2. Tests des Endpoints API (API Tests)
# ------------------------------------------------------------------------------

class LearningAPITests(APITestCase):
    def setUp(self):
        """
        Prépare un utilisateur pour l'authentification et crée des instances
        initiales de Lesson, Quiz, Question et Answer pour tester les endpoints.
        """
        self.user = User.objects.create_user(
            username="learning_api", password="apipass", email="learning_api@example.com"
        )
        self.client.login(username="learning_api", password="apipass")

        self.lesson = Lesson.objects.create(
            title="API Lesson",
            content="Contenu de la leçon créée via l'API."
        )
        self.quiz = Quiz.objects.create(
            lesson=self.lesson,
            title="API Quiz",
            instructions="Suivez bien les instructions.",
            time_limit=25
        )
        self.question = Question.objects.create(
            quiz=self.quiz,
            text="Que signifie REST ?",
            question_type="text",
            correct_answer="Representational State Transfer"
        )
        self.answer = Answer.objects.create(
            question=self.question,
            text="Representational State Transfer",
            is_correct=True
        )

    def test_list_lessons(self):
        """
        Vérifie que l'API retourne la liste des leçons.
        On suppose que le basename dans le routeur DRF est "lesson".
        """
        url = reverse("lesson-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_lesson_api(self):
        """
        Vérifie que l'on peut créer une nouvelle leçon via l'API.
        """
        url = reverse("lesson-list")
        data = {
            "title": "New API Lesson",
            "content": "Contenu de la nouvelle leçon via l'API."
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_list_quizzes(self):
        """
        Vérifie que l'API retourne la liste des quiz.
        On suppose que le basename dans le routeur DRF est "quiz".
        """
        url = reverse("quiz-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_quiz_api(self):
        """
        Vérifie que l'on peut créer un nouveau quiz via l'API.
        """
        url = reverse("quiz-list")
        data = {
            "lesson": self.lesson.id,
            "title": "New API Quiz",
            "instructions": "Nouvelles instructions pour le quiz via l'API.",
            "time_limit": 30
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Quiz.objects.filter(title="New API Quiz").count(), 1)

    def test_list_questions(self):
        """
        Vérifie que l'API retourne la liste des questions.
        On suppose que le basename dans le routeur DRF est "question".
        """
        url = reverse("question-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_question_api(self):
        """
        Vérifie que l'on peut créer une nouvelle question via l'API.
        """
        url = reverse("question-list")
        data = {
            "quiz": self.quiz.id,
            "text": "New API Question?",
            "question_type": "text",
            "correct_answer": "New correct answer"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.filter(text="New API Question?").count(), 1)

    def test_list_answers(self):
        """
        Vérifie que l'API retourne la liste des réponses.
        On suppose que le basename dans le routeur DRF est "answer".
        """
        url = reverse("answer-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_answer_api(self):
        """
        Vérifie que l'on peut créer une nouvelle réponse via l'API.
        """
        url = reverse("answer-list")
        data = {
            "question": self.question.id,
            "text": "New API Answer",
            "is_correct": False
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Answer.objects.filter(text="New API Answer").count(), 1)
