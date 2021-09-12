from rest_framework import serializers
from .models import Message, Room, User


class UserSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(source="profile.image")

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "image"]


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "text", "image", "seen", "room", "user", "timestamp"]
        extra_kwargs = {"user": {"read_only": True}, "seen": {"read_only": True}}


class RoomSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        user = self.context["request"].user
        if obj.user1 == user:
            return UserSerializer(obj.user2).data
        return UserSerializer(obj.user1).data

    class Meta:
        model = Room
        fields = ["id", "user1", "user", "timestamp"]
        extra_kwargs = {"user1": {"write_only": True}}
