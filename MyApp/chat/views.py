from rest_framework.views import APIView
from rest_framework import authentication
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from .serializers import RoomSerializer, ChatUserNoRoomsSerializer, InvitationSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Room, Invitation
from django.utils import timezone


class Rooms(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request):
        serializer = RoomSerializer(request.user.rooms.all(), many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            room = serializer.save()
            room.users.add(request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LeaveRoom(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def post(self, request):
        try:
            room = request.user.rooms.get(id=request.data["room"])
            room.users.remove(request.user)
            return Response(status=status.HTTP_200_OK)
        except Room.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CreateInvitation(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def post(self, request):
        data = {"invitor": request.user.id, "room": request.data["room"]}
        serializer = InvitationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AcceptInvitation(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def post(self, request, invitation_id):
        invitation = Invitation.objects.get(id=invitation_id)
        if invitation.room.users.contains(invitation.invitor) and not invitation.room.users.contains(
                request.user) and timezone.now() < invitation.expires_at:
            invitation.room.users.add(request.user)
            return Response(RoomSerializer(invitation.room).data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

