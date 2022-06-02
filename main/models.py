from django.db import models
from django.template.defaultfilters import truncatechars
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser

from src.utils.utils import UtilsImage
from src.utils.filters import DescriptionFilter, ImageFilter
from src.utils.validators import CustomValidators


class UserModel(AbstractUser, ImageFilter):
    telegram_chat_id = models.IntegerField(unique=True, blank=True, null=True, verbose_name="Telegram user ID")
    profile_picture = models.ImageField(
        null=True, blank=True,
        verbose_name="Your photo", validators=[CustomValidators.validate_image_expansion],
        upload_to=UtilsImage.image_name_user
    )

    @property
    def show_display(self):
        if self.profile_picture.name:
            return UtilsImage.image_url(image_url=self.profile_picture.url, method="display")
        return "Not photo"

    @property
    def show_field(self):
        if self.profile_picture.name:
            return UtilsImage.image_url(image_url=self.profile_picture.url, method="field")
        return "Not photo"

# <<<=======================================>>> Base Model <<<=======================================================>>>


class NetworkModel(models.Model, DescriptionFilter, ImageFilter):
    network: str = models.CharField(primary_key=True, verbose_name="Network name", max_length=15, unique=True)
    logo = models.ImageField(
        blank=True, null=True, verbose_name="Network logo", validators=[
            CustomValidators.validate_logo, CustomValidators.validate_image_expansion
        ], upload_to=UtilsImage.image_name_network
    )
    blockchain_url = models.URLField(blank=True, null=True, verbose_name="Blockchain URL")
    description: str = models.TextField(blank=True, null=True, verbose_name="Network description")

    def __str__(self):
        return f"{self.network}"

    def save(self, *args, **kwargs):
        self.network = self.network.upper()
        super().save(*args, **kwargs)

    @property
    def short_description(self):
        return truncatechars(self.description, 30) if len(self.description) > 30 else "Not description"

    @property
    def show_display(self):
        if self.logo.name:
            return UtilsImage.image_url(image_url=self.logo.url, method="display")
        return "Not logo"

    @property
    def show_field(self):
        if self.logo.name:
            return UtilsImage.image_url(image_url=self.logo.url, method="field")
        return "Not logo"

    class Meta:
        verbose_name = 'Network'
        verbose_name_plural = 'Networks'
        db_table = 'network_model'


class TokenModel(models.Model, DescriptionFilter, ImageFilter, DescriptionFilter):
    token: str = models.CharField(verbose_name="Token name", max_length=15)
    network: str = models.ForeignKey(
        "NetworkModel", on_delete=models.CASCADE, db_column="network", verbose_name="Network name"
    )
    logo = models.ImageField(
            blank=True, null=True, verbose_name="Token logo", validators=[CustomValidators.validate_logo]
    )
    decimals = models.IntegerField(verbose_name="Token decimals", validators=[
        MinValueValidator(0), MaxValueValidator(20)
    ])
    address = models.CharField(verbose_name="Token smart contract address")
    description: str = models.TextField(blank=True, null=True, verbose_name="Token description")
    token_info = models.JSONField(blank=True, null=True, verbose_name="Token info")

    def __str__(self):
        return f"{self.network}-{self.token}"

    @property
    def short_description(self):
        return truncatechars(self.description, 30) if len(self.description) > 30 else "Not description"

    def save(self, *args, **kwargs):
        self.token = self.token.upper()
        super().save(*args, **kwargs)

    @property
    def show_display(self):
        if self.logo.name:
            return UtilsImage.image_url(image_url=self.logo.url, method="display")
        return "Not logo"

    @property
    def show_field(self):
        if self.logo.name:
            return UtilsImage.image_url(image_url=self.logo.url, method="field")
        return "Not logo"

    class Meta:
        verbose_name = 'Token'
        verbose_name_plural = 'Tokens'
        db_table = 'token_model'
