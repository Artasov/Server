from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class User(AbstractUser):
    # username уже существует
    # first_name уже существует
    # last_name уже существует
    # password уже существует
    HWID = models.CharField(max_length=50, blank=True, null=True, default=None)

    billid = models.CharField(max_length=15, blank=True, null=True)
    pay_link = models.CharField(max_length=150, blank=True)

    money = models.IntegerField(default=0)

    promo_used = models.TextField(default="")

    date_joined = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f'{self.username}, {self.email}'


class UnconfirmedUser(models.Model):
    username = models.CharField(max_length=50, blank=True)
    password = models.CharField(max_length=250, blank=True)
    email = models.EmailField(max_length=320, blank=True)
    CODE = models.CharField(max_length=50, blank=True, null=True, default=None)
    date = models.DateTimeField(blank=True, null=True, default=datetime.now)


class UnconfirmedPasswordReset(models.Model):
    email = models.EmailField(max_length=320, blank=True)
    CODE = models.CharField(max_length=50, blank=True, null=True, default=None)
    date = models.DateTimeField(blank=True, null=True, default=datetime.now)


class File(models.Model):
    file_name = models.CharField(max_length=50)
    file = models.FileField(upload_to='files/', blank=True)

    def __str__(self):
        return f'{self.file_name}'


class Idea(models.Model):
    username = models.ForeignKey('User', on_delete=models.CASCADE)
    idea = models.TextField(blank=True,)
    date = models.DateTimeField(default=datetime.now)