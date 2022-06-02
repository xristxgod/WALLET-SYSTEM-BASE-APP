from django.utils.safestring import mark_safe


class Utils:

    @staticmethod
    def image_url(image_url: str = None, method: str = "display"):
        if image_url is None:
            return mark_safe("<img src='' width='{}' />".format(method))

        return mark_safe("<img src='{}' width='{}' />".format(
            image_url, 50 if method == "display" else 200
        ))
