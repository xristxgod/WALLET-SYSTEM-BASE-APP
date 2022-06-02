from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from main.models import UserModel
from main.models import NetworkModel, TokenModel, TransactionStatusModel


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


@admin.register(TokenModel)
class TokenModelAdmin(admin.ModelAdmin):
    fields = ("token", "network", "decimals", "address", "description", "token_info", "logo", "show_field")
    list_display = ("token", "network", "address", "show_display")
    list_display_links = ("token", "network")
    search_fields = ("token", "network", "decimals", "address")
    list_filter = ("token", "network", "decimals", "address")
    readonly_fields = ('show_field',)


@admin.register(TransactionStatusModel)
class TransactionStatusModelAdmin(admin.ModelAdmin):
    fields = ("id", "title", "description", "logo", "show_field")
    list_display = ("id", "title", "show_display")
    list_display_links = ("id", "title")
    search_fields = ("id", "title")
    list_filter = ("id", "title")
    readonly_fields = ('show_field',)
