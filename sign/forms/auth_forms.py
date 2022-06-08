from django import forms
from main.models import UserModel


class LoginAuthenticationForm(forms.ModelForm):
    """Authentication form"""
    user = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput, max_length=255)

    def clean(self):
        user_data = self.cleaned_data['user']
        password = self.cleaned_data['password']
        if UserModel.objects.filter(username=user_data).exists():
            self.cleaned_data["username"] = user_data
            data = {"username": user_data}
        elif user_data.isdigit() and UserModel.objects.filter(telegram_chat_id=int(user_data)).exists():
            self.cleaned_data["telegram_chat_id"] = user_data
            data = {"telegram_chat_id": user_data}
        else:
            raise forms.ValidationError("The user with the given username/chat_id was not found!")
        if not UserModel.objects.get(**data).check_password(password):
            raise forms.ValidationError('Invalid password')
        return self.cleaned_data

    class Meta:
        model = UserModel
        fields = ['password']


class LoginCodeForm(forms.Form):
    """Auth form"""
    code_google_auth = forms.IntegerField(max_length=6, required=False)
    code_telegram_auth = forms.IntegerField(max_length=6, required=False)
