from typing import Union

from django.utils.safestring import mark_safe
from django.db import models


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

    @staticmethod
    def temporary_password(chat_id: int) -> str:
        return f"temporary_password_{chat_id}"
