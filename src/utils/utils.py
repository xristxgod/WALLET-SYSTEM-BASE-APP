from wallet.models import ReferralModel
from django.core.exceptions import ValidationError

class CustomValidator:

    @staticmethod
    def is_have_referrer_code(code: str):
        if not ReferralModel.objects.get(referral_code=code).exists():
            raise ValidationError("This referral is not in the system!")
