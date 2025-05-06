from rest_framework import serializers
from konnected.learning.models import Lesson, Quiz, Question, Answer

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            'id',
            'title',
            'content',
            'knowledge_unit',
            'created_at',
            'updated_at'
        ]

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = [
            'id',
            'lesson',
            'title',
            'instructions',
            'time_limit',
            'created_at',
            'updated_at'
        ]

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'id',
            'quiz',
            'text',
            'question_type',
            'correct_answer',
            'created_at',
            'updated_at'
        ]

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = [
            'id',
            'question',
            'text',
            'is_correct',
            'created_at',
            'updated_at'
        ]
