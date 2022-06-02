from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from main.models import UserModel

admin.site.register(UserModel, UserAdmin)