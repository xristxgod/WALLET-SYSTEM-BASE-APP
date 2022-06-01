from django.contrib import admin

from wallet.models import (
    NetworkModel, TokenModel, TransactionStatusModel,
    UserModel, WalletModel, BalanceModel,
    TransactionModel
)
from wallet.models import AdminWithdrawModel

# <<<=============================================>>> Helper Admin <<<===============================================>>>

@admin.register(NetworkModel)
class NetworkModelAdmin(admin.ModelAdmin):
    list_display = ("network", "url")
    list_display_links = ("network", "url")
    search_fields = ("network",)
    list_filter = ("network",)

@admin.register(TokenModel)
class TokenModelAdmin(admin.ModelAdmin):
    list_display = ("token", "network", "address")
    list_display_links = ("token", "network", "address")
    search_fields = ("token", "network")
    list_filter = ("token", "network")

@admin.register(TransactionStatusModel)
class TransactionStatusModelAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    list_display_links = ("id", "title")
    search_fields = ("id", "title")
    list_filter = ("id", "title")

# <<<=============================================>>> User Admin <<<=================================================>>>

@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "first_name", "last_name", "age")
    list_display_links = ("id", "username", "first_name", "last_name", "age")
    search_fields = ("id", "username", "first_name", "last_name", "age")
    list_filter = ("id", "username", "first_name", "last_name", "age")

@admin.register(WalletModel)
class WalletModelAdmin(admin.ModelAdmin):
    list_display = ("address", "network", "user_id")
    list_display_links = ("address", "network", "user_id")
    search_fields = ("address", "network", "user_id")
    list_filter = ("address", "network", "user_id")

@admin.register(BalanceModel)
class BalanceModelAdmin(admin.ModelAdmin):
    list_display = ("balance", "network", "token", "user_id")
    list_display_links = ("network", "token", "user_id")
    search_fields = ("network", "token", "user_id")
    list_filter = ("network", "token", "user_id")

# <<<=============================================>>> Transaction Admin <<<==========================================>>>

@admin.register(TransactionModel)
class TransactionModelAdmin(admin.ModelAdmin):
    list_display = ("transaction_hash", "amount", "network", "token", "user_id")
    list_display_links = ("transaction_hash", "amount", "network", "token", "user_id")
    search_fields = ("transaction_hash", "network", "token", "user_id")
    list_filter = ("transaction_hash", "network", "token", "user_id")

# <<<=============================================>>> Admin Withdrew Admin <<<=======================================>>>

@admin.register(AdminWithdrawModel)
class AdminWithdrawModelAdmin(admin.ModelAdmin):
    list_display = ("time", "amount")
    list_display_links = ("time", "amount")
    search_fields = ("time", "amount")
    list_filter = ("time", "amount")