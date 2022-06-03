import json
from typing import Dict

from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponseRedirect

from main.models import UserModel
from sign.forms.auth_forms import LoginAuthenticationForm, LoginGoogleAuthForm
from src.utils.utils import Utils, UtilsGoogleAuth
from src.utils.types import TELEGRAM_USER_ID
from src.sender.sender_to_telegram import SenderToTelegram
from config import logger

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
                else:
                    params = json.dumps({"user_id": user.id}).encode("utf-8").hex()
                    return redirect("login_google_auth", params=params)
        return render(request, "auth/authentication_page.html", {"form": form})


class LoginGoogleAuthView(View):
    """Google auth - Additional protection for the wallet"""
    def get(self, request, *args, **kwargs):
        form = LoginGoogleAuthForm(request.POST or None)
        context = {
            "form": form
        }
        return render(request, "auth/google_auth_page.html", context)

    def post(self, request, *args, **kwargs):
        form = LoginGoogleAuthForm(request.POST or None)
        if form.is_valid():
            try:
                params: Dict = json.loads(bytes.fromhex(kwargs.get('params')).decode("utf-8"))
            except Exception as error:
                logger.error(f"ERROR: {error}")
                return redirect("login")
            user: UserModel = UserModel.objects.get(id=params.get("user_id"))
            chat_id = user.telegram_chat_id
            if UtilsGoogleAuth.is_valid_code(user.google_auth_code, form.cleaned_data["code"]):
                user = authenticate(username=user.username, password=user.password)
                login(request, user)
                # We notify the telegram bot that we have logged in!
                SenderToTelegram.auth_info(chat_id=chat_id)
                return HttpResponseRedirect("/")
            else:
                messages.add_message(request, messages.ERROR, 'Invalid code')
        return render(request, "auth/google_auth_page.html", {"form": form})
