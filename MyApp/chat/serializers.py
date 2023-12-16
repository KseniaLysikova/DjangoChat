from rest_framework import serializers
from .models import Room
from chatuser.serializers import ChatUserNoRoomsSerializer


class RoomSerializer(serializers.ModelSerializer):
    users_info = ChatUserNoRoomsSerializer(required=False, read_only=True, source='users.all', many=True)

    class Meta:
        model = Room
        fields = ["name", "users_info"]
        depth = 1
