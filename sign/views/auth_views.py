from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

from main.models import UserModel
from sign.forms.auth_forms import LoginAuthenticationForm
from src.utils.utils import Utils
from src.utils.types import TELEGRAM_USER_ID
from src.sender.sender_to_telegram import SenderToTelegram


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
            user: UserModel = UserModel.objects.get(**data)
            chat_id: TELEGRAM_USER_ID = user.telegram_chat_id
            if user.telegram_chat_id is not None and \
                    user.check_password(Utils.temporary_password(chat_id=user.telegram_chat_id)):
                # If the user does not have a password, then he is registered via Telegram.
                # You should send an SMS with the code to his Telegram account
                status = SenderToTelegram.auto_code(chat_id=chat_id)
                if status:
                    return HttpResponseRedirect("/login/telegram-auth")
            else:
                # In this case, the user has been in the system more than once and we simply authorize him.
                if user.google_auth_code is None:
                    user = authenticate(username=user.username, password=user.password)
                    login(request, user)
                    # We notify the telegram bot that we have logged in!
                    SenderToTelegram.auth_info(chat_id=chat_id)
                    return HttpResponseRedirect("/")
                return HttpResponseRedirect("/login/google-auth")
        return render(request, "auth/authentication_page.html", {"form": form})