from django.db import models
from chatuser.models import ChatUser
import datetime


# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=16)
    users = models.ManyToManyField(ChatUser, related_name="rooms", blank=True)


class Invitation(models.Model):
    room = models.ForeignKey(Room, related_name="invitations", on_delete=models.CASCADE)
    invitor = models.ForeignKey(ChatUser, on_delete=models.CASCADE)
    expires_at = models.DateField(default=datetime.datetime.now() + datetime.timedelta(days=1))
