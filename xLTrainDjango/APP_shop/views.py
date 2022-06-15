import environ
from django.shortcuts import render, redirect

from APP_home.models import User
from params_and_funcs import reCAPTCHA_validation, add_license_time
from xLTrainDjango.xLLIB_v1 import random_str
from . import qiwi
from .models import Products, Licenses

env = environ.Env()


def Shop(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('login')

        product = Products.objects.get(name=request.POST['product'])

        return render(request, 'APP_shop/buy.html', context={
            'product': product,
            'RECAPTCHA_KEY': env('GOOGLE_RECAPTCHA_SITE_KEY'),
        })

    products = Products.objects.all()
    return render(request, 'APP_shop/main_shop.html', context={
        'products': products,
    })


def Buy(request):
    if request.method == "POST":
        # reCAPTCHA
        result_reCAPTCHA = reCAPTCHA_validation(request)
        if not result_reCAPTCHA['success'] and not request.user.is_staff:
            product = Products.objects.get(name=request.POST['product'])
            return render(request, 'APP_shop/buy.html', context={
                'product': product,
                'captcha_invalid': "Invalid reCAPTCHA. Please try again.",
                'RECAPTCHA_KEY': env('GOOGLE_RECAPTCHA_SITE_KEY')
            })
        username = request.user.username
        product = Products.objects.get(name=request.POST['product'])
        user_ = User.objects.get(username=username)

        # DEL BILL IF EXIST
        if user_.billid is not None:
            bill = qiwi.check_bill(user_.billid)
            if bill['status']['value'] == 'PAID':
                return redirect('pay')
            else:
                qiwi.del_bill(user_.billid)

        # GENERATE BILL ID
        billid = random_str(15)

        # CREATING BILL
        # price
        if request.POST['price'] == 'price_week':
            price = product.price_week
        elif request.POST['price'] == 'price_month':
            price = product.price_month
        elif request.POST['price'] == 'price_6_month':
            price = product.price_6_month
        elif request.POST['price'] == 'price_forever':
            price = product.price_forever
        else:
            return render(request, 'NotFound.html')

        # activate promo-code
        promo = ""
        if request.POST['promo_code'].upper() == 'XLARTAS20':
            promo_used = user_.promo_used
            if request.POST['promo_code'].upper() in promo_used:
                return render(request, 'APP_shop/buy.html', context={
                    'product': product,
                    'invalid': "Promo-code already used.",
                    'RECAPTCHA_KEY': env('GOOGLE_RECAPTCHA_SITE_KEY')
                })
            else:
                price = price - int((price / 100) * 20)
                promo = request.POST['promo_code'].upper()

        if request.POST['promo_code'].upper() == 'XLARTAS10':
            promo_used = user_.promo_used
            if request.POST['promo_code'].upper() in promo_used:
                return render(request, 'APP_shop/buy.html', context={
                    'product': product,
                    'invalid': "Promo-code already used.",
                    'RECAPTCHA_KEY': env('GOOGLE_RECAPTCHA_SITE_KEY')
                })
            else:
                add_license_time(request.user.username, request.POST['product'], 5 * 60 * 60)
                user_.promo_used += request.POST['promo_code'].upper() + ' | '
                user_.save()
                return redirect('profile')

        response = qiwi.create_bill(value=price, product=product.name, license_time=request.POST['price'],
                                    billid=billid,
                                    promo=promo,
                                    username=request.user.username)

        # ERROR CREATING BILL
        try:
            if response['errorCode']:
                context = {
                    'name': product.name,
                    'price_week': product.price_week,
                    'price_month': product.price_month,
                    'price_6_month': product.price_6_month,
                    'price_forever': product.price_forever,
                    'RECAPTCHA_KEY': env('GOOGLE_RECAPTCHA_SITE_KEY')
                }
                return render(request, 'APP_shop/buy.html',
                              {'context': context, 'invalid': 'Error on our side, sorry'})
        except KeyError:
            pass

        # UPDATE User
        user_.pay_link = response['payUrl']
        user_.billid = billid
        user_.save()

        # REDIRECT
        return redirect('pay')


def Pay(request):
    if request.user.is_authenticated:
        user_ = User.objects.get(username=request.user.username)
        if user_.billid is not None:
            bill = qiwi.check_bill(user_.billid)
            if bill['status']['value'] == 'PAID':

                # GET PRODUCT NAME AND LICENSE TIME
                product = bill['customFields']['product']
                product_ = Products.objects.get(name=product)
                license_time = bill['customFields']['license_time']
                promo = bill['customFields']['promo']
                if promo == 'NONE':
                    promo = ''

                # ADD LICENSE TIME
                if license_time == 'price_week':
                    add_license_time(request.user.username, product, 7 * 24 * 3600)
                    user_.money += product_.price_week
                    license_ = Licenses.objects.get(username=user_, product=product_)
                    license_.product_money += product_.price_week
                elif license_time == 'price_month':
                    add_license_time(request.user.username, product, 4 * 7 * 24 * 3600)
                    user_.money += product_.price_month
                    license_ = Licenses.objects.get(username=user_, product=product_)
                    license_.product_money += product_.price_month
                elif license_time == 'price_6_month':
                    add_license_time(request.user.username, product, 6 * 4 * 7 * 24 * 3600)
                    user_.money += product_.price_6_month
                    license_ = Licenses.objects.get(username=user_, product=product_)
                    license_.product_money += product_.price_6_month
                elif license_time == 'price_forever':
                    add_license_time(request.user.username, product, 5 * 12 * 4 * 7 * 24 * 3600)
                    user_.money += product_.price_forever
                    license_ = Licenses.objects.get(username=user_, product=product_)
                    license_.product_money += product_.price_forever
                else:
                    return render(request, 'NotFound.html')

                user_.billid = None
                user_.promo_used += promo + ' | '
                user_.save()
                license_.count += 1
                license_.save()

                return redirect('profile')
            else:
                return render(request, 'APP_shop/Pay.html', {'bill': bill})
        else:
            return redirect('shop')
    else:
        return redirect('login')


def Product(request, product):
    product_ = Products.objects.get(name=product)

    return render(request, 'APP_shop/product.html', context={
        'product': product_
    })
