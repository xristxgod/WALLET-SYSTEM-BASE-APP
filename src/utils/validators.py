from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions


class CustomValidators:
    """Custom validators"""
    @staticmethod
    def validate_logo(logo):
        width, height = get_image_dimensions(logo)
        if 100 > width > 300:
            raise ValidationError("The image is %i pixel wide. It's supposed to be 200px" % width)
        elif 100 > height > 300:
            raise ValidationError("The image is %i pixel high. It's supposed to be 200px" % height)

