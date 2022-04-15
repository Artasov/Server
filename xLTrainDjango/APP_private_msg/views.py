from datetime import datetime, timedelta

import environ
from django.shortcuts import render

from params_and_funcs import log
from params_and_funcs import reCAPTCHA_validation
from xLTrainDjango.xLLIB_v1 import random_str
from .models import PrivateMsg as PrivateMsg_

# Create your views here.

env = environ.Env()


def PrivateMsgRead(request, key=None):
    log('PrivateMsg reading...START')
    msg_object = PrivateMsg_.objects.filter(key=key)
    log('PrivateMsg reading...1')
    if not msg_object.exists():
        log('PrivateMsg does not exists msg')
        log('PrivateMsg reading...END')
        return render(request, 'APP_private_msg/private-msg.html',
                      context={
                          'not_exist': 'Does not exists...',
                          'without_header': True
                      })

    log('PrivateMsg reading...2')
    fields_private_msg = dict(PrivateMsg_.objects.filter(key=key).values()[0])
    log('PrivateMsg reading...3')
    msg = fields_private_msg['msg']
    log('PrivateMsg reading...4')

    # check time for auto del
    date_for_del = msg_object[0].date_for_del
    log('PrivateMsg reading...5')
    if date_for_del < datetime.now():
        log('PrivateMsg timeout')
        msg_object.delete()
        return render(request, 'APP_private_msg/private-msg.html',
                      context={
                          'not_exist': 'Does not exists...',
                          'header_logo_only': True
                      })
    log('PrivateMsg reading...6')
    # delete and render page with read private MSG

    context = {
        'read': True,
        'msg': msg,
        'header_logo_only': True
    }

    log('PrivateMsg reading...7')
    # if files exists
    if fields_private_msg['file'] != '':
        log('PrivateMsg reading... +file')
        context['file'] = fields_private_msg['file']
        if '.png' in fields_private_msg['file'].lower() \
                or '.jpg' in fields_private_msg['file'].lower() \
                or '.jpeg' in fields_private_msg['file'].lower():
            log('PrivateMsg reading... file - img')
            context['img'] = PrivateMsg_.objects.filter(key=key)[0].file.url

    if fields_private_msg['voice_msg'] != '':
        log('PrivateMsg reading... +voice_msg')
        context['voice_msg'] = PrivateMsg_.objects.filter(key=key)[0].voice_msg.url

    msg_object.delete()

    for i in range(len(context)):
        log(f'{list(context.keys())[i]}:{context[list(context.keys())[i]]}')

    log('PrivateMsg reading...END')
    return render(request, 'APP_private_msg/private-msg.html',
                  context=context)


def PrivateMsg(request, key=None):
    # if reading msg
    if key is not None:
        context = {
            'key': key,
            'pre_read': True,
            'header_logo_only': True
        }
        return render(request, 'APP_private_msg/private-msg.html',
                      context=context)

    # If create private msg:
    if request.method == 'POST':
        log('PrivateMsg creating... START')

        # reCAPTCHA
        result_reCAPTCHA = reCAPTCHA_validation(request)
        if not result_reCAPTCHA['success']:
            log('PrivateMsg invalid recaptcha')
            log('PrivateMsg creating... END')
            return render(request, 'APP_private_msg/private-msg.html',
                          context={
                              'create': True,
                              'captcha_invalid': "Invalid reCAPTCHA. Please try again.",
                              'RECAPTCHA_KEY': env('GOOGLE_RECAPTCHA_SITE_KEY'),
                              'header_logo_only': True,
                              'msg': request.POST['msg']
                          })

        # GENERATE KEY
        KEY = random_str(length=40)

        delete_in_time = str(request.POST['delete_in_time'])
        if 'sec' in delete_in_time:
            date_for_del = datetime.now() + timedelta(seconds=int(delete_in_time.replace(" sec", "")))
        elif 'min' in delete_in_time:
            date_for_del = datetime.now() + timedelta(minutes=int(delete_in_time.replace(" min", "")))
        elif 'hour' in delete_in_time:
            date_for_del = datetime.now() + timedelta(hours=int(delete_in_time.replace(" hour", "")))
        elif 'day' in delete_in_time:
            date_for_del = datetime.now() + timedelta(days=int(delete_in_time.replace(" day", "")))
        else:
            date_for_del = datetime.now() + timedelta(days=365 * 10)

        file = request.FILES.get('file')
        voice_msg = request.FILES.get('voice_msg')

        # CHECK SIZE
        if file is not None:
            if file.size > 30 * 1024 * 1024:
                log('PrivateMsg creating... file is too big')
                log('PrivateMsg creating... END')
                return render(request, 'APP_private_msg/private-msg.html',
                              context={
                                  'create': True,
                                  'invalid': "File is too big!",
                                  'RECAPTCHA_KEY': env('GOOGLE_RECAPTCHA_SITE_KEY'),
                                  'header_logo_only': True
                              })
        if voice_msg is not None:
            if voice_msg.size > 30 * 1024 * 1024:
                log('PrivateMsg creating... voice_msg is too big')
                log('PrivateMsg creating... END')
                return render(request, 'APP_private_msg/private-msg.html',
                              context={
                                  'create': True,
                                  'invalid': "Voice msg is too big!",
                                  'RECAPTCHA_KEY': env('GOOGLE_RECAPTCHA_SITE_KEY'),
                                  'header_logo_only': True
                              })

        log('PrivateMsg creating... next step->create')

        # If sent is nothing
        if request.POST['msg'] == '' and file is None and voice_msg is None:
            print(1)
            return render(request, 'APP_private_msg/private-msg.html',
                          context={
                              'create': True,
                              'invalid': "U didn't send anything",
                              'RECAPTCHA_KEY': env('GOOGLE_RECAPTCHA_SITE_KEY'),
                              'header_logo_only': True
                          })
        PrivateMsg_.objects.create(msg=request.POST['msg'], file=file, voice_msg=voice_msg, key=KEY,
                                   date_for_del=date_for_del).save()

        link = request.get_host() + request.path + f'{KEY}/'
        log('PrivateMsg creating... success END')
        return render(request, 'APP_private_msg/private-msg.html',
                      context={
                          'link': link,
                          'RECAPTCHA_KEY': env('GOOGLE_RECAPTCHA_SITE_KEY'),
                          'header_logo_only': True
                      })
    log('PrivateMsg open')
    return render(request, 'APP_private_msg/private-msg.html',
                  context={
                      'create': 'create',
                      'RECAPTCHA_KEY': env('GOOGLE_RECAPTCHA_SITE_KEY'),
                      'header_logo_only': True
                  })
