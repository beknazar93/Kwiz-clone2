from django.db import models
from django.contrib.auth.models import User

class Quiz(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes', null=True, blank=True)
    quiz_name = models.CharField(max_length=255)
    info = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.quiz_name

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question = models.TextField()
    answer1 = models.CharField(max_length=255)
    answer2 = models.CharField(max_length=255)
    answer3 = models.CharField(max_length=255)
    answer4 = models.CharField(max_length=255)
    # Храним номер правильного ответа (1–4)
    correct_answer = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question
