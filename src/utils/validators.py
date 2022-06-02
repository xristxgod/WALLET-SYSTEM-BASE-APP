from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

from src.utils.types import CRYPTO_NETWORK, CRYPTO_ADDRESS, ADDRESS_PREFIX


class CustomValidators:
    """Custom validators"""
    @staticmethod
    def validate_logo(logo):
        width, height = get_image_dimensions(logo)
        if width > 300 or width < 100:
            raise ValidationError("The image is %i pixel wide. It's supposed to be 200px" % width)
        elif height > 300 or height < 100:
            raise ValidationError("The image is %i pixel high. It's supposed to be 200px" % height)

    @staticmethod
    def validate_image_expansion(image):
        _, extension = image.split(".")
        if extension not in ["png", "ico", "jpeg"]:
            raise ValidationError("the extension of the image: {} and should be {}.".format(
                extension, ["png", "ico", "jpeg"]
            ))

    @staticmethod
    def validate_address(network: CRYPTO_NETWORK, address: CRYPTO_ADDRESS):
        if address[0] not in ADDRESS_PREFIX[network]:
            raise ValidationError('This crypto wallet: {} should start with these sims: {}'.format(
                address, ADDRESS_PREFIX[network]
            ))
