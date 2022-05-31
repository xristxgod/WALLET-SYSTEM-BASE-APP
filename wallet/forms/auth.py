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

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    phone = forms.CharField(required=False)
    address = forms.CharField(required=False)
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].lable = 'Login'
        self.fields['first_name'].lable = 'First name'
        self.fields['last_name'].lable = 'Last name'
        self.fields['password'].lable = 'Password'
        self.fields['confirm_password'].lable = 'Confirm password'
        self.fields['phone'].lable = 'Phone number'
        self.fields['email'].lable = 'Email'

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(f"The user with this email: {email} already exists")
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'The user with this username: {username} already exists')
        return username

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('The password was entered incorrectly')
        return self.cleaned_data

    class Meta:
        model = User
        fields = [
            'username', 'first_name',
            'last_name', 'password',
            'confirm_password', 'phone',
            'address', 'email'
        ]