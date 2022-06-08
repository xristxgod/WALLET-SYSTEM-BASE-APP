import json
from typing import Dict, Tuple

from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import login
from django.contrib import messages
from django.http import HttpResponseRedirect

from main.models import UserModel
from sign.forms.auth_forms import LoginAuthenticationForm
from sign.forms.auth_forms import LoginCodeForm
from src.helper.temporary import temporary_code
from src.utils.utils import Utils, UtilsGoogleAuth, BaseUtils
from src.utils.types import TELEGRAM_USER_ID
from src.sender.sender_to_telegram import SenderToTelegram
from config import logger


def is_auth(user_id: int) -> Tuple[bool, bool]:
    user = UserModel.objects.get(id=user_id)
    return user.google_auth_code is not None, user.telegram_chat_id is not None


class LoginAuthenticationView(View):
    """Authentication view - Checks if there is a user in the system"""
    def get(self, request, *args, **kwargs):
        if BaseUtils.is_authorized(request):
            return HttpResponseRedirect("/")
        form = LoginAuthenticationForm(request.POST or None)
        context = {
            "form": form
        }
        return render(request, "auth/authentication_page.html", context)

    def post(self, request, *args, **kwargs):
        if BaseUtils.is_authorized(request):
            return HttpResponseRedirect("/")
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
                    params = json.dumps({"user_id": user.id, "chat_id": chat_id}).encode("utf-8").hex()
                    return HttpResponseRedirect("login_auth", params=params)
            else:
                # In this case, the user has been in the system more than once and we simply authorize him.
                if user.google_auth_code is None and user.telegram_chat_id is None:
                    login(request, user, backend="django.contrib.auth.backends.ModelBackend")
                    # We notify the telegram bot that we have logged in!
                    SenderToTelegram.auth_info(chat_id=chat_id)
                    return HttpResponseRedirect("/")
                else:
                    params = json.dumps({"user_id": user.id, "chat_id": chat_id}).encode("utf-8").hex()
                    return redirect("login_auth", params=params)
        return render(request, "auth/authentication_page.html", {"form": form})


class LoginAuthView(View):
    """Auth - Additional protection for the wallet"""
    def get(self, request, *args, **kwargs):
        form = LoginCodeForm(request.POST or None)
        try:
            params: Dict = json.loads(bytes.fromhex(kwargs.get('params')).decode("utf-8"))
        except Exception as error:
            logger.error(f"ERROR: {error}")
            return redirect("login")
        google_auth, telegram_auth = is_auth(user_id=params.get("user_id"))
        context = {
            "form": form,
            "googleAuth": google_auth,
            "telegramAuth": telegram_auth,
        }
        return render(request, "auth/auth_page.html", context)

    def post(self, request, *args, **kwargs):
        auth = [False, False]
        form = LoginCodeForm(request.POST or None)
        try:
            params: Dict = json.loads(bytes.fromhex(kwargs.get('params')).decode("utf-8"))
        except Exception as error:
            logger.error(f"ERROR: {error}")
            return redirect("login")
        google_auth, telegram_auth = is_auth(user_id=params.get("user_id"))
        if form.is_valid():
            user: UserModel = UserModel.objects.get(id=params.get("user_id"))

            if google_auth and "code_google_auth" in form.cleaned_data:
                if UtilsGoogleAuth.is_valid_code(user.google_auth_code, form.cleaned_data["code_google_auth"]):
                    auth[0] = True
                else:
                    messages.add_message(request, messages.ERROR, 'Google Auth is invalid code')
            else:
                auth[0] = True

            if telegram_auth and "code_telegram_auth" in form.cleaned_data:
                code = temporary_code.get_temporary_code(chat_id=params.get("char_id"))
                if code == form.cleaned_data["code_telegram_auth"]:
                    temporary_code.delete_temporary_code(chat_id=params.get("char_id"))
                    auth[1] = True
                else:
                    messages.add_message(request, messages.ERROR, 'Telegram Auth is invalid code')
            else:
                auth[1] = True

            if auth[0] and auth[1]:
                login(request, user, backend="django.contrib.auth.backends.ModelBackend")
                SenderToTelegram.auth_info(chat_id=params.get("char_id"))
                return HttpResponseRedirect("/")

        return render(request, "auth/auth_page.html", {
            "form": form,
            "googleAuth": google_auth,
            "telegramAuth": telegram_auth,
        })
