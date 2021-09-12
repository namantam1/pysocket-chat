from django.db.models import Q
from rest_framework.generics import ListCreateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Message, Room
from .serializer import MessageSerializer, RoomSerializer, UserSerializer


class ProfileView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        return Response(UserSerializer(self.request.user).data)


class RoomView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RoomSerializer

    def perform_create(self, serializer):
        return serializer.save(user2=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Room.objects.filter(Q(user1=user) | Q(user2=user))


class MessageView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        room_id = self.kwargs["room"]
        return Message.objects.filter(room=room_id).order_by("-timestamp")

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
