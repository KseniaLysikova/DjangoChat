from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

from .managers import ChatUserManager


class ChatUser(AbstractUser):
    username = models.CharField(blank=False, max_length=16)
    email = models.EmailField(unique=True)
    birthdate = models.DateField(null=True)
    profile_pic = models.ImageField(default="profile_pics/default.png", upload_to="profile_pics/")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username", "birthdate", "profile_pic"]
    objects = ChatUserManager()

