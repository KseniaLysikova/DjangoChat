from rest_framework import serializers
from chatuser.models import ChatUser


class ChatUserSerializer(serializers.ModelSerializer):
    rooms = serializers.SerializerMethodField()

    class Meta:
        model = ChatUser
        fields = ChatUser.REQUIRED_FIELDS + ['rooms']

    def get_rooms(self, obj):
        return [{"id": room.id, "name": room.name} for room in obj.rooms.all()]


class ChatUserNoRoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatUser
        fields = ChatUser.REQUIRED_FIELDS
