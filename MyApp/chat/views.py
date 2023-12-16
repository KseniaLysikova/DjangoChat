from rest_framework.views import APIView
from rest_framework import authentication
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from .serializers import ChatUserNoRoomsSerializer
from rest_framework.response import Response
from rest_framework import status


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


class Invite(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request):
        serializer = InvitationSerializer(request.user.invitations.all(), many=True)
        return Response(serializer.data)