from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import consumers
from .views import QuizViewSet, QuestionViewSet

router = DefaultRouter()
router.register(r'quizzes', QuizViewSet, basename='quiz')
router.register(r'questions', QuestionViewSet, basename='question')

urlpatterns = [
    path('', include(router.urls)),
    path("ws/quiz/<str:pin>/", consumers.QuizConsumer.as_asgi()),
]
