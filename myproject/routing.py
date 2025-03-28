# myproject/routing.py
from django.urls import re_path
from api import consumers  # обязательно убедись, что у тебя есть consumers.py в api

websocket_urlpatterns = [
    re_path(r'ws/quiz/(?P<pin>\d+)/$', consumers.QuizConsumer.as_asgi()),
]
