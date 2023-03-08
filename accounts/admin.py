from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User


class UserAdmin(DjangoUserAdmin):
    pass


admin.site.register(User, UserAdmin)
