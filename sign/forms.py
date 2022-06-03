from django import forms
from main.models import UserModel

class LoginAuthenticationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user"].lable = "Username/Telegram chat id"

    def clean(self):
        user_data = self.cleaned_data['user']
        if UserModel.objects.filter(username=user_data).exists():
            self.cleaned_data["username"] = user_data
        elif UserModel.objects.filter(telegram_chat_id=user_data).exists():
            self.cleaned_data["telegram_chat_id"] = user_data
        else:
            raise forms.ValidationError("The user with the given username/chat_id was not found!")
        return self.cleaned_data

    class Meta:
        model = UserModel
        fields = [
            'username', 'telegram_chat_id'
        ]


class LoginAuthorizationForm(forms.ModelForm):
    pass


class LoginTelegramAuthForm(forms.ModelForm):
    pass


class LoginGoogleAuthForm(forms.ModelForm):
    pass