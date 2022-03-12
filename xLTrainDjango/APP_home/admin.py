from django.contrib import admin

from .models import User, UnconfirmedUser, UnconfirmedPasswordReset


# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'nickname', 'guild', 'gender', 'HWID', 'date_joined']
    list_editable = ['nickname', 'guild', 'gender', 'HWID']


@admin.register(UnconfirmedUser)
class UnconfirmedUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'gender']


@admin.register(UnconfirmedPasswordReset)
class UnconfirmedPasswordResetAdmin(admin.ModelAdmin):
    list_display = ['email', 'CODE', 'date']
