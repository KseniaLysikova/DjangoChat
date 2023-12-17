import datetime

from django.db import models
from chatuser.models import ChatUser
from django.utils import timezone


# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=16)
    users = models.ManyToManyField(ChatUser, related_name="rooms", blank=True)


def get_default_expire_date():
    return timezone.now() + datetime.timedelta(days=1)


class Invitation(models.Model):
    room = models.ForeignKey(Room, related_name="invitations", on_delete=models.CASCADE)
    invitor = models.ForeignKey(ChatUser, on_delete=models.CASCADE)
    expires_at = models.DateTimeField(default=get_default_expire_date)


class Message(models.Model):
    room = models.ForeignKey(Room, related_name="messages", on_delete=models.CASCADE)
    author = models.ForeignKey(ChatUser, related_name="messages", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=128)

    class Meta:
        ordering = ["created"]
