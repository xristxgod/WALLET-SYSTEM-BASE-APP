from typing import Union, List, Dict

from django.utils.safestring import mark_safe
from django.db import models

from src.services.__init__ import Transaction
from src.utils.types import CRYPTO_ADDRESS


class UtilsImage:
    """Utils for image"""
    @staticmethod
    def image_url(image_url: str = None, method: str = "display"):
        if image_url is None:
            return mark_safe("<img src='' width='{}' />".format(method))

        return mark_safe("<img src='{}' width='{}' />".format(
            image_url, 50 if method == "display" else 200
        ))

    @staticmethod
    def image_name_network(instance: models.Model, filename: str) -> str:
        file_base, extension = filename.split(".")
        return "logo_%s.%s" % (instance.network.lower(), extension)

    @staticmethod
    def image_name_token(instance: models.Model, filename: str) -> str:
        file_base, extension = filename.split(".")
        return "logo_%s.%s" % (f"{instance.network.network.lower()}_{instance.token.lower()}", extension)

    @staticmethod
    def image_transaction_status(instance: models.Model, filename: str) -> str:
        file_base, extension = filename.split(".")
        return "logo_%s.%s" % (f"{instance.id}_{instance.title.lower()}", extension)

    @staticmethod
    def image_name_user(instance: models.Model, filename: str) -> str:
        file_base, extension = filename.split(".")
        return "avatar_%s.%s" % (f"{instance.id}_{instance.username.lower()}", extension)


class Utils:
    """Project utils"""
    @staticmethod
    def is_number(number: Union[float, str, int]) -> bool:
        if isinstance(number, str):
            try:
                if number.find(",") >= 0:
                    number = number.replace(",", ".")
                float(number)
                return True
            except ValueError:
                return False
        else:
            return True


class UtilsTransaction:
    """Transaction utils"""
    @staticmethod
    def get_participants_list(participants: List[Dict]) -> List[CRYPTO_ADDRESS]:
        return [address.get("address") for address in participants]

    @staticmethod
    def packaging_transactions(transactions: List[models.Model]) -> List[Transaction]:
        transactions_list: List[Transaction] = []
        for transaction in transactions:
            transactions_list.append(Transaction(
                time=transaction.time, transaction_hash=transaction.transaction_hash,
                inputs=UtilsTransaction.get_participants_list(transaction.inputs),
                outputs=UtilsTransaction.get_participants_list(transaction.outputs),
                amount=transaction.amount, fee=transaction.fee, status=transaction.status
            ))
        return transactions_list
