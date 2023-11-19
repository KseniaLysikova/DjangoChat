import json
from channels.auth import login
from channels.generic.websocket import AsyncWebsocketConsumer
import urllib
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from channels.db import database_sync_to_async


@database_sync_to_async
def get_user(token):
    return Token.objects.get(key=token).user


class WebSocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        token = urllib.parse.parse_qs(self.scope['query_string'])[b'token'][0].decode("utf-8").strip()
        user = await get_user(token)
        await login(self.scope, user)

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        # self.room_name = "chat_1"
        print(self.scope["url_route"])
        self.room_group_name = "chat_%s" % self.room_name

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = {"type": "chat_message",
                   "author": self.scope["user"].username,
                   "message": text_data_json['message']}
        await self.channel_layer.group_send(self.room_group_name, message)

    async def chat_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))
