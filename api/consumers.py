# # api/consumers.py
# import json
# from channels.generic.websocket import AsyncWebsocketConsumer

# class QuizConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.pin = self.scope['url_route']['kwargs']['pin']
#         self.room_group_name = f"quiz_{self.pin}"

#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()
#         await self.send(text_data=json.dumps({
#             "event": "room-joined",
#             "payload": f"Joined room {self.pin}"
#         }))

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 "type": "broadcast_message",
#                 "event": data.get("event"),
#                 "payload": data.get("payload")
#             }
#         )

#     async def broadcast_message(self, event):
#         await self.send(text_data=json.dumps({
#             "event": event["event"],
#             "payload": event["payload"]
#         }))

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class QuizConsumer(AsyncWebsocketConsumer):
    rooms = {}

    async def connect(self):
        self.pin = self.scope['url_route']['kwargs']['pin']
        self.room_group_name = f"quiz_{self.pin}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        if self.pin not in self.rooms:
            self.rooms[self.pin] = {
                "host": None,
                "players": [],
                "current_question": None
            }

        print(f"[WS] Подключение к комнате: {self.pin}")

    async def disconnect(self, close_code):
        room = self.rooms.get(self.pin)
        if not room:
            return

        for player in room["players"]:
            if player["channel"] == self.channel_name:
                player["connected"] = False

        if room["host"] == self.channel_name:
            room["host"] = None

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "broadcast",
                "event": "players-updated",
                "payload": [
                    {"name": p["name"], "score": p["score"]}
                    for p in room["players"] if p["connected"]
                ]
            }
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        event = data.get("event")
        payload = data.get("payload")
        room = self.rooms[self.pin]

        if event == "host-join":
            room["host"] = self.channel_name
            await self.send(json.dumps({"event": "players-updated", "payload": [
                {"name": p["name"], "score": p["score"]}
                for p in room["players"] if p["connected"]
            ]}))
        
        elif event == "player-joined":
            name = payload["name"]
            session_id = payload["sessionId"]

            player = next((p for p in room["players"]
                           if p["name"] == name and p["sessionId"] == session_id), None)

            if player:
                player["channel"] = self.channel_name
                player["connected"] = True
            else:
                room["players"].append({
                    "name": name,
                    "sessionId": session_id,
                    "channel": self.channel_name,
                    "score": 0,
                    "connected": True
                })

            await self.channel_layer.send(room["host"], {
                "type": "broadcast",
                "event": "players-updated",
                "payload": [
                    {"name": p["name"], "score": p["score"]}
                    for p in room["players"] if p["connected"]
                ]
            })

        elif event == "new-question":
            room["current_question"] = payload
            room["current_question"]["responses"] = {}
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "broadcast",
                    "event": "new-question",
                    "payload": payload
                }
            )

        elif event == "player-answer":
            name = payload["name"]
            score = payload.get("score", 0)

            player = next((p for p in room["players"]
                           if p["name"] == name and p["connected"]), None)
            if player and name not in room["current_question"]["responses"]:
                player["score"] += score
                room["current_question"]["responses"][name] = True

            leaderboard = sorted(
                [{"name": p["name"], "score": p["score"]} for p in room["players"] if p["connected"]],
                key=lambda x: (-x["score"], x["name"])
            )

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "broadcast",
                    "event": "question-results",
                    "payload": {"leaderboard": leaderboard}
                }
            )

        elif event == "game-over":
            leaderboard = sorted(
                [{"name": p["name"], "score": p["score"]} for p in room["players"]],
                key=lambda x: (-x["score"], x["name"])
            )
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "broadcast",
                    "event": "game-over",
                    "payload": {"leaderboard": leaderboard}
                }
            )

    async def broadcast(self, event):
        await self.send(text_data=json.dumps({
            "event": event["event"],
            "payload": event["payload"]
        }))

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class QuizConsumer(AsyncWebsocketConsumer):
    rooms = {}

    async def connect(self):
        self.pin = self.scope['url_route']['kwargs']['pin']
        self.room_group_name = f"quiz_{self.pin}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        if self.pin not in self.rooms:
            self.rooms[self.pin] = {
                "host": None,
                "players": [],
                "current_question": None,
                "settings": {
                    "animationSpeed": 600,
                    "timerDuration": 15,
                    "allowedStudents": []
                }
            }

        print(f"[WS] Подключение к комнате: {self.pin}")

    async def disconnect(self, close_code):
        room = self.rooms.get(self.pin)
        if not room:
            return

        for player in room["players"]:
            if player["channel"] == self.channel_name:
                player["connected"] = False

        if room["host"] == self.channel_name:
            room["host"] = None

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "broadcast",
                "event": "players-updated",
                "payload": [
                    {"name": p["name"], "score": p["score"]}
                    for p in room["players"] if p["connected"]
                ]
            }
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        event = data.get("event")
        payload = data.get("payload")
        room = self.rooms[self.pin]

        if event == "host-join":
            room["host"] = self.channel_name
            await self.send(json.dumps({
                "event": "players-updated",
                "payload": [
                    {"name": p["name"], "score": p["score"]}
                    for p in room["players"] if p["connected"]
                ]
            }))

        elif event == "allowed-students":
            room["settings"]["allowedStudents"] = [name.lower() for name in payload.get("students", [])]

        elif event == "animation-speed":
            room["settings"]["animationSpeed"] = payload.get("speed", 600)

        elif event == "timer-duration":
            room["settings"]["timerDuration"] = payload.get("duration", 15)

        elif event == "player-joined":
            name = payload["name"].strip().lower()
            session_id = payload["sessionId"]

            if room["settings"]["allowedStudents"] and name not in room["settings"]["allowedStudents"]:
                await self.send(json.dumps({
                    "event": "access-denied",
                    "payload": {"reason": "not-allowed"}
                }))
                return

            player = next((p for p in room["players"] if p["name"] == name and p["sessionId"] == session_id), None)

            if player:
                player["channel"] = self.channel_name
                player["connected"] = True
            else:
                room["players"].append({
                    "name": name,
                    "sessionId": session_id,
                    "channel": self.channel_name,
                    "score": 0,
                    "connected": True
                })

            if room["host"]:
                await self.channel_layer.send(room["host"], {
                    "type": "broadcast",
                    "event": "players-updated",
                    "payload": [
                        {"name": p["name"], "score": p["score"]}
                        for p in room["players"] if p["connected"]
                    ]
                })

        elif event == "new-question":
            room["current_question"] = payload
            room["current_question"]["responses"] = {}
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "broadcast",
                    "event": "new-question",
                    "payload": payload
                }
            )

        elif event == "player-answer":
            name = payload["name"].strip().lower()
            score = payload.get("score", 0)

            player = next((p for p in room["players"] if p["name"] == name and p["connected"]), None)
            if player and name not in room["current_question"]["responses"]:
                player["score"] += score
                room["current_question"]["responses"][name] = True

            leaderboard = sorted(
                [{"name": p["name"], "score": p["score"]} for p in room["players"] if p["connected"]],
                key=lambda x: (-x["score"], x["name"])
            )

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "broadcast",
                    "event": "question-results",
                    "payload": {"leaderboard": leaderboard}
                }
            )

        elif event == "question-timeout":
            print("[WS] Таймер вопроса истёк.")

        elif event == "game-over":
            leaderboard = sorted(
                [{"name": p["name"], "score": p["score"]} for p in room["players"]],
                key=lambda x: (-x["score"], x["name"])
            )
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "broadcast",
                    "event": "game-over",
                    "payload": {"leaderboard": leaderboard}
                }
            )

    async def broadcast(self, event):
        await self.send(text_data=json.dumps({
            "event": event["event"],
            "payload": event["payload"]
        }))

