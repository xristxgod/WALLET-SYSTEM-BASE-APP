from django.shortcuts import render
from django.views import View

class MainPageView(View):
    def get(self, request, *args, **kwargs):
        context = {
            "transactions": "Hello",
        }
        return render(request, 'main/main_page.html', context)