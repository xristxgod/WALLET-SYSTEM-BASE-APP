from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    chat_id = models.IntegerField(unique=True, blank=True, verbose_name="Telegram user ID")