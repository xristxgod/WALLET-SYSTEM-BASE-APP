from django.urls import path
from sign.views.auth_views import LoginAuthenticationView

urlpatterns = [
    path("login/", LoginAuthenticationView.as_view(), name="login"),
]
