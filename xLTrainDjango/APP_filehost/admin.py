from django.contrib import admin
from .models import Upload, UploadedFile
# Register your models here.


@admin.register(Upload)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'date_upload', 'date_delete']
    list_editable = ['username', 'date_upload', 'date_delete']


@admin.register(UploadedFile)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'upload', 'file_name', 'file_size', 'file']
    list_editable = ['upload', 'file_name', 'file_size', 'file']