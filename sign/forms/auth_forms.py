from django import forms
from main.models import UserModel


class LoginAuthenticationForm(forms.ModelForm):
    """Authentication form"""
    user = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            "class": "form-control form-control-lg",
            "type": "text",
            "id": "typeUsername"
        })
    )
    password = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput(attrs={
            "class": "form-control form-control-lg",
            "type": "password",
            "id": "typePasswordX"
        })
    )

    def clean(self):
        user_data = self.cleaned_data['user']
        password = self.cleaned_data['password']
        if UserModel.objects.filter(username=user_data).exists():
            self.cleaned_data["username"] = user_data
            data = {"username": user_data}
        elif UserModel.objects.filter(telegram_chat_id=user_data).exists():
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
    """Google auth form"""
    code = forms.CharField(max_length=6)
