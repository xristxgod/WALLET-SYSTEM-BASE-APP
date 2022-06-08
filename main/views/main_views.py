from django.shortcuts import render
from django.views import View

from main.models import TransactionModel


class MainPageView(View):
    def get(self, request, *args, **kwargs):
        context = {
            "transactions": TransactionModel.objects.all(),
        }
        return render(request, 'main/main_page.html', context)
