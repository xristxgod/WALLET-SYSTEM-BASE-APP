from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].lable = 'Login'
        self.fields['password'].lable = 'Password'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(f"User {username} is not found in system!")
        user = User.objects.filter(username=username).first()
        if user and not user.check_password(password):
            raise forms.ValidationError("Password is bad")
        return self.cleaned_data

    class Meta:
        model = User
        fields = [
            "username", "password"
        ]