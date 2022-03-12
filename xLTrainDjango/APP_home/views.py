import json
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

from APP_shop import qiwi
from APP_shop.models import UserLicense
from params_and_funcs import log, check_registration_field_correctness, EMAIL_validator, reCAPTCHA_validation
from xLTrainDjango.xLLIB_v1 import random_str, send_EMail
from .models import User, UnconfirmedUser, UnconfirmedPasswordReset


def Home(request):
    log("+ Home view START")
    if request.method == "POST":
        result = dict(request.POST)

        # POST req AFTER LOGIN
        try:
            if request.POST['next'] == '/':
                return render(request, 'xLTrainDjango/home.html')
        except KeyError:

            pass
        log('REGISTRATION')
        log("+ Home POST")
        # reCAPTCHA
        result_reCAPTCHA = reCAPTCHA_validation(request)
        if not result_reCAPTCHA['success']:
            log("- Home reCAPTCHA")
            return render(request, 'APP_home/home.html',
                          {'captcha_invalid': f"Invalid reCAPTCHA. Please try again."})
        # CHECK FORM CORRECTION
        ERROR_ARR = check_registration_field_correctness(result)
        if len(ERROR_ARR) != 0:
            log(f"- Home {ERROR_ARR}")
            return render(request, 'APP_home/home.html',
                          {'form_invalid': f"{', '.join(ERROR_ARR)}", 'error_msgs': ERROR_ARR})

        # ALREADY EXISTS
        if User.objects.filter(username=request.POST['username']).exists():
            log(f"- Home username already exist")
            return render(request, 'APP_home/home.html',
                          {'registration_fail': '1', 'username_fail': request.POST['username']})
        if User.objects.filter(email=request.POST['email']).exists():
            log('- Home email already exist')
            return render(request, 'APP_home/home.html',
                          {'registration_fail': '1', 'email_fail': request.POST['email']})

        # GENERATE CONFIRMATION CODE
        CODE = random_str(40)
        log(f'CODE {CODE}')

        # SAVE UnconfirmedUser
        UnconfirmedUser(username=request.POST['username'],
                        email=request.POST['email'],
                        gender=request.POST['gender'],
                        password=make_password(request.POST['password']),
                        CODE=CODE
                        ).save()
        log(f'UnconfirmedUser saved')

        # SEND CODE EMAIL
        subject, from_email, to = 'Completion of registration', settings.EMAIL_HOST_USER, request.POST['email']
        html_content = str(render_to_string('email_templates/email_RegistrateConfirmation.html', {'code': CODE}))
        send_EMail(25, to, subject, html_content)
        log(f'SENDED CODE to EMAIL {to}')
        log(f'+ REGISTRATION END')
        log(f'+ Home view END')

        return render(request, 'registration/registrate_confirmation.html')

    log(f'+ Home view END')
    return render(request, 'APP_home/home.html')


def RegistrateConfirmation(request):
    if request.method == "POST":
        if UnconfirmedUser.objects.filter(CODE=request.POST['CODE']).exists():
            unconfirmeduser_ = UnconfirmedUser.objects.get(CODE=request.POST['CODE'])

            # SAVE NEW USER
            User(username=unconfirmeduser_.username,
                 email=unconfirmeduser_.email,
                 gender=unconfirmeduser_.gender,
                 password=unconfirmeduser_.password,
                 HWID=None).save()
            UserLicense(username=unconfirmeduser_.username).save()
            # DEL THIS UNCONFIRMED USER
            unconfirmeduser_.delete()

            return redirect('login')
        else:
            return redirect('login')
            # return render(request, 'registration/registrate_confirmation.html', {'invalid': 'Invalid Code'})


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
    if request.method == "POST":
        # CHECKIN FOR VALID EMAIL
        if not EMAIL_validator(request.POST['email']):
            return render(request, 'registration/password_reset_stage_1.html', context={'invalid': 'Invalid email'})

        # CHECKING EMAIL EXISTS
        if not User.objects.filter(email=request.POST['email']).exists():
            return render(request, 'registration/password_reset_stage_1.html',
                          context={'invalid': 'User with this email does not exists'})

        # GENERATE CONFIRMATION CODE
        CODE = random_str(40)

        # DELETE ENTRIES WITH THIS EMAIL IF THEY EXISTS

        entries_for_del = UnconfirmedPasswordReset.objects.filter(email=request.POST['email'])
        for i in entries_for_del:
            i.delete()

        # SAVE UnconfirmedPasswordReset
        UnconfirmedPasswordReset(email=request.POST['email'],
                                 CODE=CODE
                                 ).save()

        # SEND CODE EMAIL
        subject, from_email, to = 'Password reset', settings.EMAIL_HOST_USER, request.POST['email']
        html_content = render_to_string('email_templates/email_PasswordResetCode.html', {'code': CODE})
        send_EMail(25, to, subject, html_content)

        return render(request,
                      'registration/password_reset_stage_2.html')  # Stage 2 - input confirmation CODE and new password

    return render(request, 'registration/password_reset_stage_1.html')


def PasswordResetConfirmation(request):
    if request.method == "POST":
        if UnconfirmedPasswordReset.objects.filter(CODE=request.POST['CODE']).exists():
            unconfirmedpasswordreset_ = UnconfirmedPasswordReset.objects.get(CODE=request.POST['CODE'])
            user_ = User.objects.get(email=unconfirmedpasswordreset_.email)

            # SAVE NEW PASSWORD USER
            user_.password = make_password(request.POST['new_password'])
            user_.save()

            # DEL THIS UNCONFIRMED USER
            unconfirmedpasswordreset_.delete()

            return render(request, 'registration/login.html', {'success': 'Password changed'})
        else:
            return render(request, 'registration/password_reset_stage_2.html', {'invalid': 'Invalid Code'})


def Profile(request):
    if request.user.is_authenticated:
        user_license_ = UserLicense.objects.get(username=request.user.username)

        xLUMRA_remained = int((user_license_.xLUMRA_date_end - datetime.now()).total_seconds() / 3600)
        xLGM_remained = int((user_license_.xLGM_date_end - datetime.now()).total_seconds() / 3600)
        xLCracker_remained = int((user_license_.xLCracker_date_end - datetime.now()).total_seconds() / 3600)

        print(xLUMRA_remained)
        print(xLGM_remained)
        print(xLCracker_remained)

        if xLUMRA_remained > 9600:
            xLUMRA_remained = 'FOREVER'
        elif xLUMRA_remained < 1:
            xLUMRA_remained = 'None'

        if xLGM_remained > 9600:
            xLGM_remained = 'FOREVER'
        elif xLGM_remained < 1:
            xLGM_remained = 'None'

        if xLCracker_remained > 9600:
            xLCracker_remained = 'FOREVER'
        elif xLCracker_remained < 1:
            xLCracker_remained = 'None'

        least_days = {
            'xLUMRA': xLUMRA_remained,
            'xLGM': xLGM_remained,
            'xLCracker':  xLCracker_remained,
        }
        return render(request, 'APP_home/profile.html', {'user_license_': user_license_, 'least_days': least_days})
    else:
        redirect('login')


def SetNickname(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user.username)
            user.nickname = request.POST['nickname']
            user.save()
            return redirect('profile')


def SetGuild(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user.username)
            user.guild = request.POST['guild']
            user.save()
            return redirect('profile')


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
            return render(request, 'APP_home/donate.html', {'invalid': 'You entered an incorrect value'})
        if value == 0:
            return render(request, 'APP_home/donate.html', {'invalid': 'You entered an incorrect value'})

        # reCAPTCHA
        result_reCAPTCHA = reCAPTCHA_validation(request)
        if not result_reCAPTCHA['success']:
            return render(request, 'APP_home/donate.html', {'invalid': 'Invalid Captcha'})

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
                              {'context': context, 'invalid': 'Error on our side, sorry'})
        except KeyError:
            pass
        return redirect(response['payUrl'])
    return render(request, 'APP_home/donate.html')


def About(request):
    return render(request, 'about.html')


def Resume(request):
    return render(request, 'resume.html', {'name': 'Resume'})


@csrf_exempt
@api_view(['POST'])
def ProgramAuth(request):
    log('+ ProgramAuth START')
    if request.method == "POST":
        log('+ ProgramAuth POST')
        json_date = list(dict(request.POST).keys())[0]
        data = dict(json.loads(json_date))
        for i in range(len(data)):
            log(list(data.keys())[i] + data[list(data.keys())[i]])
        user = authenticate(request, username=data['username'], password=data['password'])
        if user is not None:
            user = User.objects.get(username=data['username'])
            user_license = UserLicense.objects.get(username=data['username'])

            if (data['product'] == 'xLGM'):
                log(data['product'])
                DATE_LICENSE = user_license.xLGM_date_end
                DATE_NOW = datetime.now()
                if (DATE_LICENSE > DATE_NOW):
                    log(f'+ ProgramAuth END {data["product"]} License true')
                    return Response({'accept': True, 'HWID': user.HWID, 'nickname': user.nickname, 'guild': user.guild},
                                    headers={'Content-Type': 'application/json'})
                log(f'- ProgramAuth END {data["product"]} License timeout')
                return Response({'accept': False, 'ERROR': 'License timeout'},
                                headers={'Content-Type': 'application/json'})

            if (data['product'] == 'xLUMRA'):
                log(data['product'])
                DATE_LICENSE = user_license.xLUMRA_date_end
                DATE_NOW = datetime.now()
                if (DATE_LICENSE > DATE_NOW):
                    log(f'+ ProgramAuth END {data["product"]} License true')
                    return Response({'accept': True, 'HWID': user.HWID, 'nickname': user.nickname, 'guild': user.guild},
                                    headers={'Content-Type': 'application/json'})
                log(f'- ProgramAuth END {data["product"]} License timeout')
                return Response({'accept': False, 'ERROR': 'License timeout'},
                                headers={'Content-Type': 'application/json'})

            if (data['product'] == 'xLCracker'):
                log(data['product'])
                DATE_LICENSE = user_license.xLCracker_date_end
                DATE_NOW = datetime.now()
                if (DATE_LICENSE > DATE_NOW):
                    log(f'+ ProgramAuth END {data["product"]} License true')
                    return Response({'accept': True, 'HWID': user.HWID, 'nickname': user.nickname, 'guild': user.guild},
                                    headers={'Content-Type': 'application/json'})
                log(f'- ProgramAuth END {data["product"]} License timeout')
                return Response({'accept': False, 'ERROR': 'License timeout'},
                                headers={'Content-Type': 'application/json'})

            if (data['product'] == 'xLHWID'):
                log(data['product'])
                if user.HWID == None:
                    user.HWID = data['HWID']
                    user.save()
                    log(f'+ ProgramAuth END {data["product"]} FIRST')
                    return Response({'accept': True, 'FIRST': True},
                                    headers={'Content-Type': 'application/json'})
                log(f'+ ProgramAuth END {data["product"]}')
                return Response({'accept': True, },
                                headers={'Content-Type': 'application/json'})

        else:
            log(f'- ProgramAuth END Login or password invalid')
            return Response({'accept': False, 'ERROR': 'Login or password invalid'},
                            headers={'Content-Type': 'application/json'})
    else:
        log(f'- ProgramAuth END Invalid request')
        return Response({'accept': False, 'ERROR': 'Invalid request'}, headers={'Content-Type': 'application/json'})


@csrf_exempt
@api_view(['POST'])
def SetHWID(request):
    log(f'+ SetHWID START')
    if request.method == "POST":
        log(f'+ SetHWID POST')
        json_date = list(dict(request.POST).keys())[0]
        data = dict(json.loads(json_date))
        user = authenticate(request, username=data['username'], password=data['password'])
        if user is not None:
            user = User.objects.get(username=data['username'])

            if (data['product'] == 'xLHWID'):
                user.HWID = data['HWID']
                user_license = UserLicense.objects.get(username=data['username'])
                user_license.xLGM_date_end = datetime.now()
                user_license.xLUMRA_date_end = datetime.now()
                user_license.xLCracker_date_end = datetime.now()
                user_license.save()
                user.save()
                log(f'+ SetHWID END HWID have been setted for {user.username}')
                return Response({'accept': True, },
                                headers={'Content-Type': 'application/json'})
            else:
                log(f'+ SetHWID END something go wrong1')
                return redirect('home')

        else:
            log('+ SetHWID END Login or pass invalid')
            return Response({'accept': False, 'ERROR': 'Login or pass invalidы'},
                            headers={'Content-Type': 'application/json'})
    else:
        log(f'+ SetHWID END something go wrong2')
        return Response({'accept': False, 'ERROR': 'Something go wrong'}, headers={'Content-Type': 'application/json'})
