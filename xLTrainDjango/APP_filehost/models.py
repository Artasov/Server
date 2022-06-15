import os

from django.conf import settings
from django.db import models
from datetime import datetime, timedelta

from transliterate import translit

from params_and_funcs import log
from xLTrainDjango.xLLIB_v1 import random_str


def format_filehost_upload(instance, filename):
    filename = translit(str(filename), language_code='ru', reversed=True).replace(' ', '_')
    return os.path.join("files/filehost/", random_str(10, alphabet='0123456789') + '_' + str(filename))


def NowPlusSevenDays():
    return datetime.utcnow() + timedelta(days=7)


class Upload(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)
    size = models.IntegerField(blank=True, default=None, null=True)
    date_upload = models.DateTimeField(default=datetime.now)
    date_delete = models.DateTimeField(default=NowPlusSevenDays)


class UploadedFile(models.Model):
    upload = models.ForeignKey('Upload', on_delete=models.CASCADE, blank=True)
    file = models.FileField(upload_to=format_filehost_upload, blank=True)
    file_name = models.CharField(max_length=200, blank=True, default=None, null=True)
    file_size = models.IntegerField(blank=True, default=None, null=True)
