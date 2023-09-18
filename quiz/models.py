from django.db import models
from user.models import User  # Assurez-vous que cela est correctement importé depuis votre modèle d'utilisateur

CHOICES = (
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
)

class Quiz(models.Model):
    title = models.CharField(max_length=255)
    article_id = models.IntegerField(null=True, blank=True)
    description = models.TextField(max_length=255,null=True, blank=True )

    def __str__(self):
        return self.title

class Question(models.Model):
    text = models.CharField(max_length=1000)
    correct_answer = models.CharField(max_length=1, choices=CHOICES)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.text
    def answers(self):
        return Answer.objects.filter(question=self)

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=5000)
    option = models.CharField(max_length=1, choices=CHOICES)

    def __str__(self):
        return f"{self.question.text} - {self.option}"


class Résultat(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='résultats')
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Utilisez le modèle User de Django
    score = models.FloatField()

    def __str__(self):
        return f"Quiz: {self.quiz}, User: {self.user}, Score: {self.score}%"