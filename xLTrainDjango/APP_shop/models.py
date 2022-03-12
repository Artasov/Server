from datetime import datetime

from django.db import models


class Products(models.Model):
    name = models.CharField(max_length=50, blank=True)
    version = models.CharField(max_length=30, default=None)
    desc = models.TextField(blank=True)
    review_ulr = models.CharField(max_length=200, null=True, blank=True)

    price_week = models.IntegerField(null=True, blank=True)
    price_month = models.IntegerField(null=True, blank=True)
    price_6_month = models.IntegerField(null=True, blank=True)
    price_forever = models.IntegerField(null=True, blank=True)

    date_update = models.DateTimeField(default=datetime.now)

    distr = models.FileField(upload_to='files/', default="", blank=True)

    def __str__(self):
        return f'{self.name}'


class UserLicense(models.Model):
    username = models.CharField(max_length=150)

    xLGM_date_end = models.DateTimeField(blank=True, null=True, default=datetime.now)
    xLGM_count = models.IntegerField(default=0)

    xLUMRA_date_end = models.DateTimeField(blank=True, null=True, default=datetime.now)
    xLUMRA_count = models.IntegerField(default=0)

    xLCracker_date_end = models.DateTimeField(blank=True, null=True, default=datetime.now)
    xLCracker_count = models.IntegerField(default=0)

    billid = models.CharField(max_length=15, blank=True, null=True)
    pay_link = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return f'{self.username}'
