# # api/routing.py
# from django.urls import re_path
# from . import consumers

# websocket_urlpatterns = [
#     re_path(r'ws/quiz/(?P<pin>\d+)/$', consumers.QuizConsumer.as_asgi()),
# ]
# yourapp/routing.py
from django.urls import re_path
from . import consumers  # consumers.py должен быть в этом же app

websocket_urlpatterns = [
    re_path(r"ws/game/(?P<pin>\w+)/$", consumers.GameConsumer.as_asgi()),
]
