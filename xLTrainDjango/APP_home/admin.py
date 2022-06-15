from django.contrib import admin

from .models import User, UnconfirmedUser, UnconfirmedPasswordReset, File, Idea


# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'money', 'promo_used', 'HWID', 'pay_link']
    list_editable = ['email', 'money', 'HWID', 'pay_link']


@admin.register(UnconfirmedUser)
class UnconfirmedUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']


@admin.register(UnconfirmedPasswordReset)
class UnconfirmedPasswordResetAdmin(admin.ModelAdmin):
    list_display = ['email', 'CODE', 'date']


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'file']
    list_editable = ['file']


@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):
    list_display = ['username', 'idea', 'date']
    list_editable = ['idea', 'date']
