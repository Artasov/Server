from django.db import models


class Item(models.Model):
    item_number = models.IntegerField(blank=True)
    color = models.CharField(choices=[('BLUE', 'BLUE'), ('RED', 'RED'), ('GREEN', 'GREEN')], blank=True, max_length=15)
