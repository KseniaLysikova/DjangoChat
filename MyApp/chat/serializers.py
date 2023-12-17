from rest_framework import serializers
from .models import *
from drf_spectacular.utils import extend_schema_serializer

class ChatUserNoRoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatUser
        fields = ChatUser.REQUIRED_FIELDS


class RoomSerializer(serializers.ModelSerializer):
    users_info = ChatUserNoRoomsSerializer(required=False, read_only=True, source='users.all', many=True)

    class Meta:
        model = Room
        fields = ["id", "name", "users_info"]
        depth = 1


class RoomNoUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id", "name"]


class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        exclude = ["expires_at"]
