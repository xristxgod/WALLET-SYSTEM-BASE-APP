from django.utils.safestring import mark_safe
from django.db import models

class UtilsImage:

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