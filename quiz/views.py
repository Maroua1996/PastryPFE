from django.shortcuts import render, redirect
from .models import Quiz, Question, Answer, Résultat
from django.contrib.auth.decorators import login_required

@login_required
def quiz_home(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quizz/quizz_home.html', {'quizzes': quizzes})

@login_required
def quiz_detail(request, quiz_id):
    quiz = Quiz.objects.get(pk=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    return render(request, 'quizz/quizz_detail.html', {'quiz': quiz, 'questions': questions})



@login_required
def submit_quiz(request, quiz_id):
    if request.method == 'POST':
        quiz = Quiz.objects.get(pk=quiz_id)
        questions = Question.objects.filter(quiz=quiz)
        user_score = 0  # Initialise le score de l'utilisateur à zéro
        user_answers = {}  # Dictionnaire pour stocker les réponses de l'utilisateur

        for question in questions:
            selected_option = request.POST.get(f'question_{question.id}', '')
            print(f"Question: {question.text}, Correct Answer: {question.correct_answer}, Selected Option: {selected_option}")
            if selected_option == question.correct_answer:
                user_score += 1  # Incrémente le score si la réponse est correcte
                user_answers[question] = True  # Stocke la réponse comme correcte
            else:
                user_answers[question] = False  # Stocke la réponse comme incorrecte

        # Débogage : Affichez le score, les réponses correctes et les réponses sélectionnées
        print(f"User: {request.user}")
        print(f"Quiz: {quiz}")
        print(f"User Score: {user_score}")
        print(f"User Answers: {user_answers}")

        # Enregistre le résultat dans la base de données
        resultat = Résultat.objects.create(quiz=quiz, user=request.user, score=user_score)
        resultat.save()
        # Calcul du score en pourcentage
        percentage_score = (user_score / len(questions)) * 100


        return render(request, 'quizz/quizz_results.html', {
            'quiz': quiz,
            'user_score': user_score,
            'total_questions': len(questions),
            'user_answers': user_answers,
            'percentage_score': percentage_score,
        })
    else:
        return redirect('quizz_detail', quiz_id=quiz_id)


@login_required
def quiz_results(request, quiz_id):
    quiz = Quiz.objects.get(pk=quiz_id)
    user_result = Résultat.objects.filter(quiz=quiz, user=request.user).first()
    
    # Vérifiez si l'utilisateur a un résultat pour ce quiz
    if user_result:
        return render(request, 'quizz/quizz_results.html', {'quiz': quiz, 'user_result': user_result})
    else:
        # Gérez le cas où l'utilisateur n'a pas pris ce quiz
        return redirect('quiz_detail', quiz_id=quiz_id)
