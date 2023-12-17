from rest_framework import serializers
from chatuser.models import ChatUser
from chat.serializers import RoomNoUsersSerializer


class ChatUserSerializer(serializers.ModelSerializer):
    rooms = RoomNoUsersSerializer(required=False, read_only=True, source="rooms.all", many=True)

    class Meta:
        model = ChatUser
        fields = ChatUser.REQUIRED_FIELDS + ['rooms']


