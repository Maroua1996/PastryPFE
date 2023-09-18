from django.urls import path
from . import views

urlpatterns = [
    path('quiz_home/', views.quiz_home, name="quiz_home"),
    path('quizz/<int:quiz_id>/', views.quiz_detail, name="quiz_detail"),
    path('quizz/<int:quiz_id>/submit/', views.submit_quiz, name="submit_quiz"),
    path('quizz/<int:quiz_id>/results/', views.quiz_results, name="quizz_results"),
]
