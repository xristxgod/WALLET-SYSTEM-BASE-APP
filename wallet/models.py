from typing import List
from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from src.utils.types import CoinsHelper
from config import logger


UserModel = get_user_model()

# <<<=============================================>>> Helper Table <<<===============================================>>>

class NetworkModel(models.Model):
    network = models.CharField(primary_key=True, max_length=255, null=False, unique=True, verbose_name="Network name")
    url = models.URLField(max_length=255, null=True, blank=True, verbose_name="Blockchain url")
    descriptions = models.TextField(null=True, blank=True, verbose_name="Network Descriptions")

    def __str__(self):
        return self.network

    class Meta:
        verbose_name = 'Network'
        verbose_name_plural = 'Networks'
        db_table = 'network_model'


class TokenModel(models.Model):
    token = models.CharField(max_length=255, null=False, verbose_name="Token name")
    network: NetworkModel = models.ForeignKey(
        'NetworkModel', on_delete=models.CASCADE, db_column="network", verbose_name="Network name"
    )
    decimals = models.IntegerField(verbose_name="Decimals")
    address = models.CharField(max_length=255, null=False, unique=True, verbose_name="Smart contract address")
    descriptions = models.TextField(null=True, blank=True, verbose_name="Token Descriptions")
    token_info = models.JSONField(null=True, blank=True, verbose_name="Additional information about the token")

    def __str__(self):
        return f"{self.network.network}-{self.token}"

    class Meta:
        verbose_name = 'Token'
        verbose_name_plural = 'Tokens'
        db_table = 'token_model'


class TransactionStatusModel(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    title = models.CharField(max_length=255, null=False, verbose_name="Title")
    description = models.TextField(null=True, blank=True, verbose_name="Transaction status descriptions")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Transaction status'
        verbose_name_plural = 'Transaction statuses'
        db_table = 'transaction_status_model'

# <<<=============================================>>> User <<<=======================================================>>>

class TelegramUserModel(models.Model):
    """Username"""
    id = models.IntegerField(
        primary_key=True, unique=True, verbose_name="Telegram chat id",
        help_text="Chat id from telegram, you can get it only in telegram!"

    )
    username = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Telegram username",
        help_text="The username from telegram, you can get it only in telegram!"
    )
    owner_id = models.ForeignKey(UserModel, verbose_name='User', on_delete=models.CASCADE, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.username.find("@") == -1:
            self.username = f"@{self.username}"
        super(self).save(*args, **kwargs)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Telegram user'
        verbose_name_plural = 'Telegram users'
        db_table = 'telegram_user_model'


class WalletModel(models.Model):
    address = models.CharField(max_length=255, null=False, unique=True, verbose_name="Wallet address")
    private_key = models.CharField(max_length=255, null=False, unique=True, verbose_name="Wallet private key")
    public_key = models.CharField(max_length=255, null=True, blank=True, unique=True, verbose_name="Wallet public key")
    passphrase = models.CharField(max_length=255, null=True, blank=True, verbose_name="Wallet passphrase")
    mnemonic_phrase = models.CharField(
        max_length=255, null=True, blank=True, unique=True, verbose_name="Wallet mnemonic phrase"
    )
    network: NetworkModel = models.ForeignKey(
        'NetworkModel', on_delete=models.CASCADE, db_column="network", verbose_name="Network name"
    )
    user_id: UserModel = models.ForeignKey(
        'UserModel', on_delete=models.CASCADE, db_column="user_id", verbose_name="Who owner?"
    )

    def save(self, *args, **kwargs):
        try:
            tokens: List[TokenModel] = TokenModel.objects.filter(network=self.network.network)
            balance_native = BalanceModel(wallet=self.id, network=self.network.network, user_id=self.user_id.id)
            balance_native.save()
            for token in tokens:
                balance = BalanceModel(
                    wallet=self.id, network=self.network.network,
                    token=token.token, user_id=self.user_id.id
                )
                balance.save()
            super(self).save(*args, **kwargs)
        except Exception as error:
            logger.error(f"ERROR: {error}")

    def __str__(self):
        return f"{self.network.network} | {self.user_id.username}"

    class Meta:
        verbose_name = 'Wallet'
        verbose_name_plural = 'Wallets'
        db_table = 'wallet_model'


class BalanceModel(models.Model):
    balance = models.DecimalField(default=0, decimal_places=6, max_digits=18, verbose_name="Balance")
    wallet: WalletModel = models.ForeignKey(
        'WalletModel', on_delete=models.CASCADE, db_column="wallet", verbose_name="Wallet"
    )
    token: TokenModel = models.ForeignKey(
        'TokenModel', on_delete=models.CASCADE, db_column="token",
        null=True, blank=True, verbose_name="Token name"
    )
    network: NetworkModel = models.ForeignKey(
        'NetworkModel', on_delete=models.CASCADE,
        db_column="network", verbose_name="Network name"
    )
    user_id: UserModel = models.ForeignKey(
        'UserModel', on_delete=models.CASCADE, db_column="user_id", verbose_name="User"
    )

    def save(self, *args, **kwargs):
        if self.token is not None and (self.network.network == self.token.token) and \
                (self.user_id.id == self.wallet.user_id.id):
            super(self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user_id.username} | {self.network.network}-{self.token.token}"

    class Meta:
        verbose_name = 'Balance'
        verbose_name_plural = 'Balances'
        db_table = 'balance_model'

# <<<=============================================>>> Transaction <<<================================================>>>

class TransactionModel(models.Model):
    time = models.IntegerField(verbose_name="Transaction confirmation time")
    transaction_hash = models.CharField(max_length=255, unique=True, default="-", verbose_name="Transaction hash")
    fee = models.DecimalField(default=0, decimal_places=6, max_digits=18, verbose_name="Transaction commission")
    amount = models.DecimalField(default=0, decimal_places=6, max_digits=18, verbose_name="Transaction amount")
    inputs = models.JSONField(null=True, blank=True, verbose_name="Sender/s")
    outputs = models.JSONField(null=True, blank=True, verbose_name="Recipient/s")
    network: NetworkModel = models.ForeignKey(
        'NetworkModel', on_delete=models.CASCADE,
        db_column="network", verbose_name="Network name"
    )
    token: TokenModel = models.ForeignKey(
        'TokenModel', on_delete=models.CASCADE,
        db_column="token", null=True, blank=True,
        verbose_name="Token name"
    )
    status: TransactionStatusModel = models.ForeignKey(
        'TransactionStatusModel', on_delete=models.CASCADE,
        db_column="status", verbose_name="Transaction status"
    )
    user_id: UserModel = models.ForeignKey(
        'UserModel', on_delete=models.CASCADE,
        db_column="user_id", verbose_name="Who owner?"
    )

    def save(self, *args, **kwargs):
        if self.token is not None and (self.token.network == self.network.network):
            super(self).save(*args, **kwargs)

    def __str__(self):
        token = self.token.token if self.token is not None else CoinsHelper.get_native_by_network(
            network=self.network.network
        )
        return f"{self.network.network}-{token} | {self.user_id.username}"

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        db_table = 'transaction_model'

# <<<=============================================>>> Admin Model <<<================================================>>>

class AdminWithdrawModel(models.Model):
    time: int = models.IntegerField(verbose_name="Withdraw time")
    amount = models.DecimalField(default=0, decimal_places=6, max_digits=18, verbose_name="Withdraw amount")
    user_ids = models.JSONField(verbose_name="User ids")

    def __str__(self):
        return f"{datetime.fromtimestamp(self.time)} | Users count: {len(self.user_ids)}"

    class Meta:
        verbose_name = 'Admin Withdraw'
        verbose_name_plural = 'Admin Withdraws'
        db_table = 'admin_withdraw_model'

# <<<=============================================>>> Referral Model <<<==============================================>>>

class ReferralModel(models.Model):
    pass