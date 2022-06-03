from django.shortcuts import render
from django.views.generic import View

from main.models import UserModel
from sign.forms import LoginAuthenticationForm


class LoginAuthenticationView(View):
    """Authentication view - Checks if there is a user in the system"""
    def get(self, request, *args, **kwargs):
        form = LoginAuthenticationForm(request.POST or None)
        context = {
            "form": form
        }
        return render(request, "auth/authentication_page.html", context)

    def post(self, request, *args, **kwargs):
        form = LoginAuthenticationForm(request.POST or None)
        if form.is_valid():
            if form.cleaned_data.get("username") is not None:
                data = {"username": form.cleaned_data["username"]}
            else:
                data = {"telegram_chat_id": form.cleaned_data["telegram_chat_id"]}

            user: UserModel = UserModel.objects.filter(**data).exists()
            if user.password is None:
                # If the user does not have a password, then he is registered via Telegram.
                # You should send an SMS with the code to his Telegram account
                pass
            else:
                # The user has a password so you can follow the usual scenario
                pass
        return render(request, "auth/authentication_page.html", {"form": form})


class LoginAuthorizationView(View):
    pass