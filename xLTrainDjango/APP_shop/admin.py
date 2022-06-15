from django.contrib import admin

from .models import Products, Licenses


# Register your models here.


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['name', 'long_name', 'version', 'date_update', 'desc', 'log']
    list_editable = ['long_name', 'version', 'date_update', 'desc', 'log']
    filter_horizontal = ['distrs']


@admin.register(Licenses)
class LicensesAdmin(admin.ModelAdmin):
    list_display = ['username', 'product', 'date_end', 'product_money', 'count']
    list_editable = ['product', 'date_end', 'product_money', 'count']

