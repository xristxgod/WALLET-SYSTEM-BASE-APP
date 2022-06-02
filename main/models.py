from django.db import models
from django.contrib.auth.models import AbstractUser

class UserModel(AbstractUser):
    telegram_chat_id = models.IntegerField(unique=True, blank=True, null=True, verbose_name="Telegram user ID")
    profile_picture = models.ImageField(null=True, blank=True, verbose_name="Your photo")

# <<<=======================================>>> Base Model <<<=======================================================>>>

class NetworkModel(models.Model):
    network: str = models.CharField(primary_key=True, verbose_name="Network name", max_length=15, unique=True)
    logo = models.ImageField(blank=True, null=True, verbose_name="Network logo")
    blockchain_url = models.URLField(blank=True, null=True, verbose_name="Blockchain URL")
    description = models.TextField(blank=True, null=True, verbose_name="Network description")

    def __str__(self):
        return f"{self.network}"

    def save(self, *args, **kwargs):
        self.network = self.network.title()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Network'
        verbose_name_plural = 'Networks'
        db_table = 'network_model'