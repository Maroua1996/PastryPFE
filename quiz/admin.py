# admin.py
from django.contrib import admin
from .models import Quiz, Question, Answer, Résultat

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1  # Number of empty Question forms to display

class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'quiz', 'correct_answer']
    list_filter = ['quiz']
    search_fields = ['text']

class AnswerAdmin(admin.ModelAdmin):
    list_display = ['question', 'text', 'option']
    list_filter = ['question__quiz']
    search_fields = ['question__text', 'text']

class RésultatAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'user', 'score']
    list_filter = ['quiz']
    search_fields = ['quiz__title', 'user__username']

# Register your models with the custom admin classes
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Résultat, RésultatAdmin)
