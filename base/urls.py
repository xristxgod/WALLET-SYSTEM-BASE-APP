from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('/', include("main.urls")),
    path('api/', include("api.urls")),
    path('sign/', include("sign.urls")),
]

