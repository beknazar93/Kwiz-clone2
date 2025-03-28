# api/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/quiz/(?P<pin>\d+)/$', consumers.QuizConsumer.as_asgi()),
]
