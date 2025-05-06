# apps/konnected/learning/admin.py

from django.contrib import admin
from konnected.learning.models import Lesson, Quiz, Question, Answer

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'knowledge_unit', 'created_at')
    search_fields = ('title', 'content')
    ordering = ('title',)

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson', 'time_limit', 'created_at')
    list_filter = ('lesson',)
    search_fields = ('title',)
    ordering = ('title',)

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1
    fields = ('text', 'is_correct')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('short_text', 'quiz', 'question_type', 'created_at')
    list_filter = ('question_type', 'quiz')
    search_fields = ('text',)
    ordering = ('quiz',)
    inlines = [AnswerInline]

    def short_text(self, obj):
        return (obj.text[:75] + '...') if len(obj.text) > 75 else obj.text
    short_text.short_description = "Question"

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'text', 'is_correct', 'created_at')
    list_filter = ('is_correct', 'question')
    search_fields = ('text',)
    ordering = ('question',)
