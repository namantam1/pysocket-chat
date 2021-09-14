from django.db.models import Q
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Message, Room, User
from .serializer import MessageSerializer, RoomSerializer, UserSerializer


class ProfileView(RetrieveAPIView):
    """
    Get profile of authenticated user
    """

    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, *args, **kwargs):
        return Response(self.get_serializer(self.request.user).data)


class Pagination(PageNumberPagination):
    page_size = 100


class UserListCreateView(ListCreateAPIView):
    """
    User list and create

    - Get list of user searched
    - Sigup user

    @query_params: search -> Search query
    """

    serializer_class = UserSerializer
    pagination_class = Pagination

    def get_queryset(self):
        search_param = self.request.query_params.get("search", "")
        return User.objects.filter(
            Q(username__iexact=search_param)
            | Q(email__iexact=search_param)
            | Q(first_name__icontains=search_param)
        ).order_by("username")


class RoomView(ListCreateAPIView):
    """
    Room list of autheticated user and create a new room.
    """

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
    """
    Messages list of a room.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        room_id = self.kwargs["room"]
        return Message.objects.filter(room=room_id).order_by("-timestamp")

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
