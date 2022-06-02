from django.db import models
from django.template.defaultfilters import truncatechars
from django.contrib.auth.models import AbstractUser

from src.utils.utils import Utils
from src.utils.filters import DescriptionFilter, ImageFilter
from src.utils.validators import CustomValidators


class UserModel(AbstractUser, ImageFilter):
    telegram_chat_id = models.IntegerField(unique=True, blank=True, null=True, verbose_name="Telegram user ID")
    profile_picture = models.ImageField(null=True, blank=True, verbose_name="Your photo")

    @property
    def show_display(self):
        if self.profile_picture.name:
            return Utils.image_url(image_url=self.profile_picture.url, method="display")
        return "Not photo"

    @property
    def show_field(self):
        if self.profile_picture.name:
            return Utils.image_url(image_url=self.profile_picture.url, method="field")
        return "Not photo"

# <<<=======================================>>> Base Model <<<=======================================================>>>


class NetworkModel(models.Model, DescriptionFilter, ImageFilter):
    network: str = models.CharField(primary_key=True, verbose_name="Network name", max_length=15, unique=True)
    logo = models.ImageField(
        blank=True, null=True, verbose_name="Network logo", validators=[CustomValidators.validate_logo]
    )
    blockchain_url = models.URLField(blank=True, null=True, verbose_name="Blockchain URL")
    description = models.TextField(blank=True, null=True, verbose_name="Network description")

    def __str__(self):
        return f"{self.network}"

    def save(self, *args, **kwargs):
        self.network = self.network.title()
        super().save(*args, **kwargs)

    @property
    def short_description(self):
        return truncatechars(self.description, 30)

    @property
    def show_display(self):
        if self.logo.name:
            return Utils.image_url(image_url=self.logo.url, method="display")
        return "Not logo"

    @property
    def show_field(self):
        if self.logo.name:
            return Utils.image_url(image_url=self.logo.url, method="field")
        return "Not logo"

    class Meta:
        verbose_name = 'Network'
        verbose_name_plural = 'Networks'
        db_table = 'network_model'