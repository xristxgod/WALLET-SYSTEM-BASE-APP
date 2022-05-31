from django.shortcuts import render
from django.views.generic import DetailView, View

from wallet.forms.auth import LoginForm

class LoginView(View):
    """Login"""
    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {
            "form": form
        }
        return render(request, 'login.html', context)