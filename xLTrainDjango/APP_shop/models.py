from datetime import datetime

from django.conf import settings
from django.db import models
from APP_home.models import File, User


class Products(models.Model):
    name = models.CharField(max_length=50, blank=True)
    long_name = models.CharField(max_length=50, blank=True)
    version = models.IntegerField(default=1)
    desc = models.TextField(blank=True)
    review_ulr = models.CharField(max_length=200, null=True, blank=True)

    price_week = models.IntegerField(null=True, blank=True)
    price_month = models.IntegerField(null=True, blank=True)
    price_6_month = models.IntegerField(null=True, blank=True)
    price_forever = models.IntegerField(null=True, blank=True)

    log = models.TextField(blank=True, null=True)

    date_update = models.DateTimeField(default=datetime.now)

    distrs = models.ManyToManyField(File)

    def __str__(self):
        return f'{self.name}'


class Licenses(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    date_end = models.DateTimeField(blank=True, null=True, default=datetime.utcnow)

    count = models.IntegerField(default=0)
    product_money = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.username} - {self.product}'
