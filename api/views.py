from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Quiz, Question
from .serializers import QuizSerializer, QuestionSerializer

class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    # При создании квиза устанавливаем host (если пользователь авторизован)
    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(host=self.request.user)
        else:
            serializer.save(host=None)

    # Дополнительный эндпоинт для обновления только информации квиза
    @action(detail=True, methods=['put'])
    def update_info(self, request, pk=None):
        quiz = self.get_object()
        new_name = request.data.get('quiz_name')
        new_info = request.data.get('info')
        if new_name and new_info:
            quiz.quiz_name = new_name
            quiz.info = new_info
            quiz.save()
            return Response(QuizSerializer(quiz).data)
        return Response({"error": "All fields must be completed"}, status=status.HTTP_400_BAD_REQUEST)

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
