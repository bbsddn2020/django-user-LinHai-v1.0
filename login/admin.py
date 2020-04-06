from django.contrib import admin

from login import models
from login.models import User


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'c_time')


admin.site.register(User, UserAdmin)
admin.site.register(models.ConfirmString)