# api/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class QuizConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.pin = self.scope['url_route']['kwargs']['pin']
        self.room_group_name = f"quiz_{self.pin}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        await self.send(text_data=json.dumps({
            "event": "room-joined",
            "payload": f"Joined room {self.pin}"
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "broadcast_message",
                "event": data.get("event"),
                "payload": data.get("payload")
            }
        )

    async def broadcast_message(self, event):
        await self.send(text_data=json.dumps({
            "event": event["event"],
            "payload": event["payload"]
        }))
