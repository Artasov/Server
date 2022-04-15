from django.contrib import admin

from .models import Products, UserLicense

# Register your models here.


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['name', 'version', 'date_update', 'desc']
    list_editable = ['version', 'date_update', 'desc']
    filter_horizontal = ['distrs']


@admin.register(UserLicense)
class UserLicenseAdmin(admin.ModelAdmin):
    list_display = ['username', 'xLGM_date_end', 'xLGM_count', 'xLUMRA_date_end', 'xLUMRA_count', 'xLCracker_date_end',
                    'xLCracker_count', 'billid', 'pay_link']
    list_editable = ['xLGM_date_end', 'xLGM_count', 'xLUMRA_date_end', 'xLUMRA_count', 'xLCracker_date_end',
                     'xLCracker_count']

