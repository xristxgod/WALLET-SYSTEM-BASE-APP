from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from main.models import UserModel
from main.models import NetworkModel


@admin.register(UserModel)
class UserModelAdmin(UserAdmin):
    model = UserModel

    add_fieldsets = (
        *UserAdmin.add_fieldsets,
        (
            "Photo",
            {
                "fields": (
                    "profile_picture",
                )
            }
        ),
        (
            "Telegram info",
            {
                "fields": (
                    "telegram_chat_id",
                )
            }
        ),
    )

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            "Photo",
            {
                "fields": (
                    "profile_picture",
                )
            }
        ),
        (
            "Telegram info",
            {
                "fields": (
                    "telegram_chat_id",
                )
            }
        )
    )


@admin.register(NetworkModel)
class NetworkModelAdmin(admin.ModelAdmin):
    list_display = ("network", "blockchain_url", "logo")
    list_display_links = ("network", "blockchain_url", "logo")
    search_fields = ("network",)
    list_filter = ("network",)