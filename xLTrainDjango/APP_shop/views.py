import os

from django.conf import settings
from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render, redirect

from APP_home.models import User
from params_and_funcs import reCAPTCHA_validation
from params_and_funcs import set_license, get_price
from xLTrainDjango.xLLIB_v1 import random_str
from . import qiwi
from .models import Products, UserLicense


def Shop(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            products = Products.objects.all()
            context = {}

            for product in products:
                context[product.name] = {
                    'name': product.name,
                    'desc': str(product.desc)[0:90] + '...',
                    'price': product.price_week,
                }
            return render(request, 'APP_shop/main_shop.html', {'reg_need': '1', 'context': context})
        product = Products.objects.get(name=request.POST['product'])

        if User.objects.get(username=request.user.username).guild == "":
            return render(request, 'APP_home/profile.html', context={'warr': 'Fill in the Guild field'})
        if User.objects.get(username=request.user.username).nickname == "":
            return render(request, 'APP_home/profile.html', context={'warr': 'Fill in the Nickname field'})

        context = {
            'name': product.name,
            'price_week': product.price_week,
            'price_month': product.price_month,
            'price_6_month': product.price_6_month,
            'price_forever': product.price_forever,
        }
        return render(request, 'APP_shop/buy.html', {'context': context})

    products = Products.objects.all()
    context = {}

    for product in products:
        context[product.name] = {
            'name': product.name,
            'desc': str(product.desc)[0:97] + '...',
            'price': product.price_week,
        }

    return render(request, 'APP_shop/main_shop.html', context={'context': context})


def Buy(request):
    if request.method == "POST":

        # reCAPTCHA
        result_reCAPTCHA = reCAPTCHA_validation(request)
        if not result_reCAPTCHA['success']:
            product = Products.objects.get(name=request.POST['product'])
            context = {
                'name': product.name,
                'price_week': product.price_week,
                'price_month': product.price_month,
                'price_6_month': product.price_6_month,
                'price_forever': product.price_forever,
                'captcha_invalid': "Invalid reCAPTCHA. Please try again.",
            }
            return render(request, 'APP_shop/buy.html', {'context': context})

        username = request.user.username
        product = request.POST['product']
        license_time = request.POST['price']
        user_license = UserLicense.objects.get(username=username)

        # DEL BILL IF EXIST
        if user_license.billid is not None:
            bill = qiwi.check_bill(user_license.billid)
            if bill['status']['value'] == 'PAID':
                return redirect('pay')
            qiwi.del_bill(user_license.billid)

        # GENERATE BILL ID
        billid = random_str(15)

        # CREATING BILL
        price = get_price(product, license_time)
        response = qiwi.create_bill(value=price, product=product, license_time=license_time, billid=billid,
                                    username=request.user.username)

        # ERROR CREATING BILL
        try:
            if response['errorCode']:
                product = Products.objects.get(name=product)
                print(response)
                context = {
                    'name': product.name,
                    'price_week': product.price_week,
                    'price_month': product.price_month,
                    'price_6_month': product.price_6_month,
                    'price_forever': product.price_forever,
                }
                return render(request, 'APP_shop/buy.html',
                              {'context': context, 'invalid': 'Error on our side, sorry'})
        except KeyError:
            pass

        # UPDATE UserLicense
        user_license.pay_link = response['payUrl']
        user_license.billid = billid
        user_license.save()

        # REDIRECT
        return redirect('pay')


def Pay(request):
    if request.user.is_authenticated:
        user_license_ = UserLicense.objects.get(username=request.user.username)
        if user_license_.billid is not None:
            bill = qiwi.check_bill(user_license_.billid)
            if bill['status']['value'] == 'PAID':

                # GET PRODUCT NAME AND LICENSE TIME
                product = bill['customFields']['product']
                license_time = bill['customFields']['license_time']

                # ADD LICENSE TIME
                set_license(user_license_, product, license_time)
                user_license_.billid = None
                if product == 'xL Guild Manager':
                    user_license_.xLGM_count = user_license_.xLGM_count + 1
                if product == 'xLUMRA':
                    user_license_.xLUMRA_count = user_license_.xLUMRA_count + 1
                if product == 'xLCracker':
                    user_license_.xLCracker_count = user_license_.xLCracker_count + 1
                user_license_.save()
                return redirect('profile')
            else:
                return render(request, 'APP_shop/Pay.html', {'bill': bill})
        else:
            return redirect('shop')
    else:
        return redirect('login')


def Product(request):
    if 'xLGM' in request.path:
        product_ = Products.objects.get(name='xL Guild Manager')
    elif 'xLUMRA' in request.path:
        product_ = Products.objects.get(name='xLUMRA')
    elif 'xLCracker' in request.path:
        product_ = Products.objects.get(name='xLCracker')
    else:
        return HttpResponseNotFound('WTF')
    return render(request, 'APP_shop/product.html', context={
        'name': product_.name,
        'desc': product_.desc,
        'price_week': product_.price_week,
        'date_update': product_.date_update,
        'version': product_.version,
        'review_ulr': product_.review_ulr,
        'distr': product_.distr
    })


def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/distr")
            response['Content-Disposition'] = 'inline;filename=' + os.path.basename(file_path)
            return response
    raise HttpResponseNotFound
