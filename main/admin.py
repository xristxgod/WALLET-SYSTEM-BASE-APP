from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from main.models import UserModel
from main.models import NetworkModel


@admin.register(UserModel)
class UserModelAdmin(UserAdmin):
    model = UserModel
    list_display = (*UserAdmin.list_display, "show_display")
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
                    "show_field"
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
    readonly_fields = (*UserAdmin.readonly_fields, 'show_field',)


@admin.register(NetworkModel)
class NetworkModelAdmin(admin.ModelAdmin):
    fields = ("network", "blockchain_url", "description", "logo", "show_field")
    list_display = ("network", "blockchain_url", "show_display")
    list_display_links = ("network", "blockchain_url")
    search_fields = ("network",)
    list_filter = ("network",)
    readonly_fields = ('show_field',)
