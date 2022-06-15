import json
import os
from datetime import datetime
import environ
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from APP_shop import qiwi
from APP_shop.models import Licenses, Products
from params_and_funcs import log, check_registration_field_correctness, EMAIL_validator, reCAPTCHA_validation
from xLTrainDjango.xLLIB_v1 import random_str, send_EMail
from .models import User, UnconfirmedUser, UnconfirmedPasswordReset, Idea

env = environ.Env()

def Home(request):
    return render(request, 'APP_home/home.html')


def Registration(request):
    if request.user.is_authenticated:
        logout(request)

    if request.method == "POST":
        # reCAPTCHA
        result_reCAPTCHA = reCAPTCHA_validation(request)
        if not result_reCAPTCHA['success']:
            return render(request, 'registration/registration.html', context={
                'captcha_invalid': 'Invalid reCAPTCHA. Please try again.',
                'username': request.POST['username'],
                'email': request.POST['email'],
                'RECAPTCHA_KEY': env('GOOGLE_RECAPTCHA_SITE_KEY'),
            })

        # CHECK FORM CORRECTION
        ERROR_ARR = check_registration_field_correctness(dict(request.POST))
        if len(ERROR_ARR) != 0:
            return render(request, 'registration/registration.html', context={
                'invalid': ' '.join(ERROR_ARR.values()),
                'username': request.POST['username'],
                'email': request.POST['email'],
                'RECAPTCHA_KEY': env('GOOGLE_RECAPTCHA_SITE_KEY'),
            })

        # ALREADY EXISTS
        if User.objects.filter(username=request.POST['username']).exists():
            return render(request, 'registration/registration.html', context={
                'invalid': 'User with this name already exists.',
                'username': request.POST['username'],
                'email': request.POST['email'],
                'RECAPTCHA_KEY': env('GOOGLE_RECAPTCHA_SITE_KEY'),
            })
        if User.objects.filter(email=request.POST['email']).exists():
            return render(request, 'registration/registration.html', context={
                'invalid': 'User with such an email already exists.',
                'username': request.POST['username'],
                'email': request.POST['email'],
                'RECAPTCHA_KEY': env('GOOGLE_RECAPTCHA_SITE_KEY'),
            })

        # GENERATE CONFIRMATION CODE
        CODE = random_str(40)

        # SAVE UnconfirmedUser
        UnconfirmedUser(username=request.POST['username'],
                        email=request.POST['email'],
                        password=make_password(request.POST['password']),
                        CODE=CODE
                        ).save()

        # SEND CODE EMAIL
        subject, from_email, to = 'Completion of registration', settings.EMAIL_HOST_USER, request.POST['email']
        html_content = str(render_to_string('email_templates/email_RegistrateConfirmation.html', context={
            'CODE': CODE,
            'DOMAIN': request.get_host()
        }))
        send_EMail(25, to, subject, html_content)

        return render(request, 'check_email.html')

    return render(request, 'registration/registration.html', context={
        'RECAPTCHA_KEY': env('GOOGLE_RECAPTCHA_SITE_KEY'),
    })


def RegistrateConfirmation(request, CODE):
    if request.user.is_authenticated:
        logout(request)
    if UnconfirmedUser.objects.filter(CODE=CODE).exists():
        unconfirmeduser_ = UnconfirmedUser.objects.get(CODE=CODE)

        # SAVE NEW USER
        User(username=unconfirmeduser_.username,
             email=unconfirmeduser_.email,
             password=unconfirmeduser_.password,
             HWID=None).save()

        # DEL THIS UNCONFIRMED USER
        unconfirmeduser_.delete()

        return render(request, 'registration/login.html', context={
            'success': 'You have successfully registered.'
        })
    else:
        return render(request, 'NotFound.html')


def Login(request):
    # CHECKING FOR LOGIN RETRY
    if request.user.is_authenticated:
        return redirect('home')
    # POST
    if request.method == "POST":
        # CHECKING EMAIL OR USERNAME LOGINING
        if ('@' in request.POST['username']):
            username_ = User.objects.get(email=request.POST['username']).username
        else:
            username_ = request.POST['username']

        user = authenticate(request, username=username_, password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'registration/login.html', context={'invalid': 'Invalid username or password'})

    return render(request, 'registration/login.html')


def Logout(request):
    logout(request)
    return redirect('home')


def PasswordReset(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('password_reset')

    if request.method == "POST":

        # reCAPTCHA
        result_reCAPTCHA = reCAPTCHA_validation(request)
        if not result_reCAPTCHA['success']:
            return render(request, 'registration/password_reset_stage_1.html', context={
                'captcha_invalid': "Invalid reCAPTCHA. Please try again.",
                'RECAPTCHA_KEY': env('GOOGLE_RECAPTCHA_SITE_KEY'),
            })

        # CHECKING FOR VALID EMAIL
        if not EMAIL_validator(request.POST['email']):
            return render(request, 'registration/password_reset_stage_1.html', context={
                'invalid': 'Invalid email',
                'RECAPTCHA_KEY': env('GOOGLE_RECAPTCHA_SITE_KEY')
            })

        # CHECKING EMAIL EXISTS
        if not User.objects.filter(email=request.POST['email']).exists():
            return render(request, 'registration/password_reset_stage_1.html', context={
                'invalid': 'User with this email does not exists',
                'RECAPTCHA_KEY': env('GOOGLE_RECAPTCHA_SITE_KEY')
            })

        # GENERATE CONFIRMATION CODE
        CODE = random_str(40)

        # SAVE UnconfirmedPasswordReset
        UnconfirmedPasswordReset(email=request.POST['email'],
                                 CODE=CODE
                                 ).save()

        # SEND CODE EMAIL
        subject, from_email, to = 'Password reset', settings.EMAIL_HOST_USER, request.POST['email']
        html_content = str(render_to_string('email_templates/email_PasswordResetCode.html', context={
            'CODE': CODE,
            'DOMAIN': request.get_host()
        }))
        send_EMail(25, to, subject, html_content)

        return render(request, 'check_email.html')

    return render(request, 'registration/password_reset_stage_1.html',
                  {'RECAPTCHA_KEY': env('GOOGLE_RECAPTCHA_SITE_KEY')})


def PasswordResetConfirmation(request, CODE):
    if request.user.is_authenticated:
        return redirect('logout')

    if request.method == "POST":
        if UnconfirmedPasswordReset.objects.filter(CODE=CODE).exists():
            unconfirmedpasswordreset_ = UnconfirmedPasswordReset.objects.get(CODE=CODE)
            user_ = User.objects.get(email=unconfirmedpasswordreset_.email)

            # SAVE NEW PASSWORD USER
            user_.password = make_password(request.POST['new_password'])
            user_.save()

            # DEL THIS UNCONFIRMED USER
            unconfirmedpasswordreset_.delete()

            return render(request, 'registration/login.html', {'success': 'Password changed'})
        else:
            return render(request, 'NotFound.html')

    return render(request, 'registration/password_reset_stage_2.html', context={
        'CODE': CODE
    })


def Profile(request):
    if request.user.is_authenticated:
        user_ = User.objects.get(username=request.user.username)
        user_licenses = Licenses.objects.filter(username=user_)
        least_days = {}

        for license in user_licenses:
            remained = int((license.date_end - datetime.utcnow()).total_seconds() / 3600)
            if remained > 9600:
                remained = 'FOREVER'
            elif remained < 1:
                remained = 'None'
            least_days[Products.objects.get(id=license.product_id).long_name] = remained

        return render(request, 'APP_home/profile.html', {'least_days': least_days})
    else:
        redirect('login')


def Terms_and_conditions(request):
    return render(request, 'terms_and_conditions.html')


def Privacy_policy(request):
    return render(request, 'privacy_policy.html')


def Donate(request):
    if request.method == "POST":
        value = request.POST['value']

        # CHECK CORRECTION
        try:
            value = int(value)
        except ValueError:
            return render(request, 'APP_home/donate.html', {'invalid': 'You entered an incorrect value',
                                                            'RECAPTCHA_KEY': env('GOOGLE_RECAPTCHA_SITE_KEY')})
        if value == 0:
            return render(request, 'APP_home/donate.html', {'invalid': 'You entered an incorrect value',
                                                            'RECAPTCHA_KEY': env('GOOGLE_RECAPTCHA_SITE_KEY')})

        # reCAPTCHA
        result_reCAPTCHA = reCAPTCHA_validation(request)
        if not result_reCAPTCHA['success']:
            return render(request, 'APP_home/donate.html', {'invalid': 'Invalid Captcha',
                                                            'RECAPTCHA_KEY': env('GOOGLE_RECAPTCHA_SITE_KEY')})

        # GENERATE BILL ID
        billid = random_str(15)

        # CREATING BILL
        response = qiwi.create_bill(value=value,
                                    product=f'Donate by {request.user.username}. Comment: {request.POST["comment"]}',
                                    license_time='none',
                                    billid=billid,
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
                return render(request, 'APP_home/donate.html',
                              {'context': context,
                               'invalid': 'Error on our side, sorry',
                               'RECAPTCHA_KEY': env('GOOGLE_RECAPTCHA_SITE_KEY')})
        except KeyError:
            pass
        return redirect(response['payUrl'])
    return render(request, 'APP_home/donate.html', {'RECAPTCHA_KEY': env('GOOGLE_RECAPTCHA_SITE_KEY')})


def About(request):
    return render(request, 'about.html')


def Resume(request):
    return render(request, 'resume.html', {'name': 'Resume'})


def Ideas(request):
    if not request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        # reCAPTCHA
        result_reCAPTCHA = reCAPTCHA_validation(request)
        if not result_reCAPTCHA['success']:
            return render(request, 'ideas.html',
                          {'captcha_invalid': "Invalid reCAPTCHA. Please try again.",
                           'RECAPTCHA_KEY': env('GOOGLE_RECAPTCHA_SITE_KEY'),
                           'idea': request.POST["idea"]})

        Idea.objects.create(username=User.objects.get(username=request.user.username), idea=request.POST['idea']).save()
        return render(request, 'ideas.html',
                      context={'success': 'Sent', 'RECAPTCHA_KEY': env('GOOGLE_RECAPTCHA_SITE_KEY')})

    return render(request, 'ideas.html', {'RECAPTCHA_KEY': env('GOOGLE_RECAPTCHA_SITE_KEY')})


def Download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)

    delete_bool = 'private' in path

    if os.path.exists(file_path):
        fh = open(file_path, 'rb')
        response = HttpResponse(fh.read(), content_type="application/distrs")
        response['Content-Disposition'] = 'inline;filename=' + os.path.basename(file_path)
        fh.close()

        if delete_bool:
            os.remove(file_path)
            delete_bool = False

        return response

    return render(request, 'NotFound.html')


def MoreView(request):
    return render(request, 'APP_home/more.html')