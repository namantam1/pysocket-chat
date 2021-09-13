from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Message, Room, User


class UserSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(source="profile.image", required=False)
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="A user with that email already exists.",
            )
        ]
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "image",
            "password",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        profile = validated_data.pop("profile", None)
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        if profile.get("image"):
            user.profile.image = profile["image"]
            user.profile.save()

        return user


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
