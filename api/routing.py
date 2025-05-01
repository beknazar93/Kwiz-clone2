# # api/routing.py
# from django.urls import re_path
# from . import consumers

# websocket_urlpatterns = [
#     re_path(r'ws/quiz/(?P<pin>\d+)/$', consumers.QuizConsumer.as_asgi()),
# ]
from django.urls import re_path
from .consumers import QuizConsumer

websocket_urlpatterns = [
    re_path(r"ws/quiz/(?P<pin>\d+)/$", QuizConsumer.as_asgi()),
]
