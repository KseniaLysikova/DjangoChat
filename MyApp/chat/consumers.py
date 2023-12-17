import json
from channels.auth import login
from channels.generic.websocket import AsyncWebsocketConsumer
import urllib
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from channels.db import database_sync_to_async
from .models import Room, Message
from chatuser.models import ChatUser


@database_sync_to_async
def get_messages(room):
    return list(room.messages.values())


@database_sync_to_async
def get_user(token):
    return Token.objects.get(key=token).user


@database_sync_to_async
def get_user_by_id(id):
    return ChatUser.objects.get(id=id)


@database_sync_to_async
def is_user_in_room(room, user):
    return room.users.contains(user)


@database_sync_to_async
def get_room(room_id):
    return Room.objects.get(id=room_id)


@database_sync_to_async
def create_message(message, room, user):
    message = Message(message=message, room=room, author=user)
    message.save()
    return message


class WebSocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = None
        token = urllib.parse.parse_qs(self.scope['query_string'])[b'token'][0].decode("utf-8").strip()
        try:
            self.user = await get_user(token)
            await login(self.scope, self.user)
            room_id = self.scope["url_route"]["kwargs"]["room_name"]

            self.room = await get_room(room_id)
            if not await is_user_in_room(self.room, self.user):
                await self.close()
                return None
            self.room_group_name = f"chat_{room_id}"
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
            messages = await get_messages(self.room)
            for message in messages:
                author = await get_user_by_id(message['author_id'])
                await self.send(json.dumps({"type": "chat_message",
                                            "author": author.username,
                                            "message": message["message"],
                                            "created": message["created"].strftime("%HH:%MM")}))
        except Token.DoesNotExist:
            await self.close()
            return None
        except Room.DoesNotExist:
            await self.close()
            return None

    async def disconnect(self, close_code):
        if self.room_group_name is not None:
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = await create_message(text_data_json['message'], self.room, self.user)
        message = {"type": "chat_message",
                   "author": message.author.username,
                   "message": message.message,
                   "created": message.created.strftime("%HH:%MM")}
        await self.channel_layer.group_send(self.room_group_name, message)

    async def chat_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))
