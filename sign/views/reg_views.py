from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth import authenticate, login

from main.models import UserModel
from sign.forms.reg_forms import RegistrationForm
from config import logger


class RegistrationView(View):
    """Registration View - Registration of a new user"""
    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        context = {
            "form": form
        }
        return render(request, "reg/registration_page.html", context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            data = {
                "username": form.cleaned_data["username"],
                "password": form.cleaned_data["password"],
                "telegram_chat_id": form.cleaned_data["telegram_chat_id"] if "telegram_chat_id" in form.cleaned_data \
                    else None
            }
            try:
                user = UserModel(**data)
                user.save()
            except Exception as error:
                logger.error(f"ERROR: {error}")
                messages.add_message(request, messages.ERROR, 'What went wrong. Try again later')
                return redirect("registration")
            user = authenticate(username=user.username, password=user.password)
            login(request, user)
            return HttpResponseRedirect("/")
        return render(request, "reg/registration_page.html", {"form": form})
