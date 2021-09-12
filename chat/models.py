from django.db import models

from django.contrib.auth import get_user_model
from uuid import uuid4

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="media", default="media/default.webp")
    last_seen = models.DateTimeField(null=True)


class Room(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)
    user1 = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="user1_rooms",
    )
    user2 = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="user2_rooms",
    )
    timestamp = models.DateTimeField(auto_now=True)

    def join_room(self, user: User):
        self.user2 = user
        self.save()
        return self


class Message(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)
    text = models.TextField(null=True, blank=True)
    image = models.URLField(null=True, blank=True)
    seen = models.BooleanField(default=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
