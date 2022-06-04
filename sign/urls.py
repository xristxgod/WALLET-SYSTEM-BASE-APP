from django.urls import path
from django.contrib.auth.views import LogoutView

from sign.views.auth_views import LoginAuthenticationView, LoginAuthView
from sign.views.reg_views import RegistrationView

urlpatterns = [
    path("login/", LoginAuthenticationView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path("login/auth/<str:params>", LoginAuthView.as_view(), name="login_auth"),
    path("registration/", RegistrationView.as_view(), name="registration"),
]
