"""
File: apps/konnected/konnected_learning/models.py

This module defines models for interactive lessons, quizzes, and assessments.
It includes models for lessons, quizzes, questions, and answers.
"""

from django.db import models
from common.base_models import BaseModel

class Lesson(BaseModel):
    """
    Represents an interactive lesson.
    """
    title = models.CharField(max_length=255, help_text="Title of the lesson.")
    content = models.TextField(help_text="Lesson content, which may include rich text, images, and video links.")
    # Optionally associate a lesson with a knowledge unit.
    knowledge_unit = models.ForeignKey(
        "foundation.KnowledgeUnit",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lessons",
        help_text="Associated knowledge unit, if any."
    )

    def __str__(self):
        return self.title

class Quiz(BaseModel):
    """
    Represents a quiz associated with a lesson.
    """
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="quizzes",
        help_text="Lesson associated with this quiz."
    )
    title = models.CharField(max_length=255, help_text="Title of the quiz.")
    instructions = models.TextField(help_text="Quiz instructions or guidelines.")
    time_limit = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Time limit in minutes, if applicable."
    )

    def __str__(self):
        return f"{self.title} (Quiz for {self.lesson.title})"

class Question(BaseModel):
    """
    Represents a question in a quiz.
    """
    QUESTION_TYPE_CHOICES = [
        ('text', 'Text'),
        ('multiple_choice', 'Multiple Choice'),
    ]
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="questions",
        help_text="Quiz to which this question belongs."
    )
    text = models.TextField(help_text="The question text.")
    question_type = models.CharField(
        max_length=20,
        choices=QUESTION_TYPE_CHOICES,
        default='text',
        help_text="Type of question."
    )
    correct_answer = models.TextField(
        null=True,
        blank=True,
        help_text="Correct answer for the question (if applicable)."
    )

    def __str__(self):
        return f"Question: {self.text[:50]}..."

class Answer(BaseModel):
    """
    Represents an answer option for a multiple choice question.
    """
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="answers",
        help_text="The question this answer belongs to."
    )
    text = models.TextField(help_text="Answer option text.")
    is_correct = models.BooleanField(
        default=False,
        help_text="Indicates if this is the correct answer."
    )

    def __str__(self):
        return f"Answer: {self.text[:50]}{' (Correct)' if self.is_correct else ''}"
