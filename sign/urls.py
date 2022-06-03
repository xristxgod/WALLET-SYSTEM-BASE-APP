from django.urls import path
from sign.views.auth_views import LoginAuthenticationView, LoginGoogleAuthView

urlpatterns = [
    path("login/", LoginAuthenticationView.as_view(), name="login"),
    path("login/google-auth/<str:params>", LoginGoogleAuthView.as_view(), name="login_google_auth"),
    # path("login/telegram-auth", "", name="login"),
]
