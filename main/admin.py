from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from main.models import UserModel

@admin.register(UserModel)
class UserModelAdmin(UserAdmin):
    model = UserModel

    add_fieldsets = (
        *UserAdmin.add_fieldsets,
        (
            "Telegram info",
            {
                "fields": (
                    "telegram_chat_id",
                )
            }
        )
    )

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            "Telegram info",
            {
                "fields": (
                    "telegram_chat_id",
                )
            }
        )
    )