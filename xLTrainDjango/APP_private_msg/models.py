import os
from datetime import datetime, timedelta
from django.db import models
from xLTrainDjango.xLLIB_v1 import random_str


def format_private_file_upload(instance, filename):
    return os.path.join("files/private_msg/", random_str(10, alphabet='0123456789') + '_' + filename)


def NowPlusSevenDays():
    return datetime.utcnow() + timedelta(days=7)


class PrivateMsg(models.Model):
    msg = models.TextField(blank=True, default=None, null=True)
    file = models.FileField(upload_to=format_private_file_upload, blank=True)
    voice_msg = models.FileField(upload_to=format_private_file_upload, blank=True)
    key = models.CharField(max_length=40)
    date_create = models.DateTimeField(default=datetime.now)
    date_for_del = models.DateTimeField(default=NowPlusSevenDays)
