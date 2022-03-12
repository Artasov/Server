from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class User(AbstractUser):
    # username уже существует
    # first_name уже существует
    # last_name уже существует
    # password уже существует
    nickname = models.CharField(max_length=25, blank=True)
    guild = models.CharField(max_length=25, blank=True)
    gender = models.CharField(max_length=1, blank=True)
    HWID = models.CharField(max_length=50, blank=True, null=True, default=None)
    date_joined = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f'{self.username}, {self.nickname}, {self.email}, {self.gender}'


class UnconfirmedUser(models.Model):
    username = models.CharField(max_length=50, blank=True)
    password = models.CharField(max_length=250, blank=True)
    email = models.EmailField(max_length=320, blank=True)
    gender = models.CharField(max_length=1, blank=True)
    CODE = models.CharField(max_length=50, blank=True, null=True, default=None)
    date = models.DateTimeField(blank=True, null=True, default=datetime.now)


class UnconfirmedPasswordReset(models.Model):
    email = models.EmailField(max_length=320, blank=True)
    CODE = models.CharField(max_length=50, blank=True, null=True, default=None)
    date = models.DateTimeField(blank=True, null=True, default=datetime.now)
