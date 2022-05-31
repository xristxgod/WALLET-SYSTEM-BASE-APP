from django.views.generic import DetailView, View

class LoginView(View):
    """Login"""
    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)