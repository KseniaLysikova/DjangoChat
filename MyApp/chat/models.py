from django.db import models
from chatuser.models import ChatUser


# Create your models here.
class Room(models.Model):
    rooms = models.ManyToManyField(ChatUser)
