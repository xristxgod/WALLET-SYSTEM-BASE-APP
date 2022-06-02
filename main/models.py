from django.db import models
from django.contrib.auth.models import AbstractUser

class UserModel(AbstractUser):
    telegram_chat_id = models.IntegerField(unique=True, blank=True, null=True, verbose_name="Telegram user ID")