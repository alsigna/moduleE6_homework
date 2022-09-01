from django.contrib.auth.models import User
from django.db import models


class Room(models.Model):
    title = models.CharField(max_length=256, unique=True)
    users = models.ManyToManyField(User, related_name="rooms", through="RoomsUsers")
    is_private = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title


class Message(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages")

    def __str__(self) -> str:
        if len(self.text) > 32:
            return self.text[:32] + "..."
        else:
            return self.text


class RoomsUsers(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
