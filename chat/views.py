from django.db.models import Q
from rest_framework.generics import ListCreateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from url_filter.integrations.drf import DjangoFilterBackend

from .models import Message, Room, User
from .serializer import MessageSerializer, RoomSerializer, UserSerializer


class ProfileView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        return Response(UserSerializer(self.request.user).data)


class Pagination(PageNumberPagination):
    page_size = 100


class UserListCreateView(ListCreateAPIView):
    serializer_class = UserSerializer
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend]
    filter_fields = ["username", "email"]

    def get_queryset(self):
        return User.objects.all().order_by("username")


class RoomView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RoomSerializer

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

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
