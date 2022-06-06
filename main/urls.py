from django.urls import path
from main.views.main_views import MainPageView

urlpatterns = [
    path("", MainPageView.as_view(), name="main")
]