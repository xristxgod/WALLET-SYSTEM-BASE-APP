from django import forms

from main.models import UserModel


class RegistrationForm(forms.ModelForm):
    """Registration form"""
    password = forms.CharField(widget=forms.PasswordInput, max_length=255)
    confirm_password = forms.CharField(widget=forms.PasswordInput, max_length=255)
    telegram_chat_id = forms.IntegerField(required=False)

    def clean_username(self):
        username = self.cleaned_data["username"]
        if UserModel.objects.filter(username=username).exists():
            raise forms.ValidationError(f"The user with this '{username}' is already in the system!")
        return username

    def clean_telegram_chat_id(self):
        telegram_chat_id = self.cleaned_data["telegram_chat_id"]
        if isinstance(telegram_chat_id, str) and not telegram_chat_id.isdigit():
            raise forms.ValidationError(f"Telegram ID must be a number!")
        return telegram_chat_id

    def clean(self):
        password, confirm_password = self.cleaned_data["password"], self.cleaned_data["confirm_password"]
        if password != confirm_password:
            raise forms.ValidationError('The password was entered incorrectly')
        return self.cleaned_data

    class Meta:
        model = UserModel
        fields = ['username', 'password', 'confirm_password', 'telegram_chat_id']
