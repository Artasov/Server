import json
import os
import re
import urllib
from datetime import datetime, timedelta

from django.conf import settings

from APP_home.models import User
from APP_private_msg.models import PrivateMsg
from APP_shop.models import Products, Licenses
from xLTrainDjango import settings


def check_registration_field_correctness(result: dict):
    RFS = {  # Registration Field Setting
        'username': [1, 50],
        'password': [1, 50],
        'first_name': [1, 50],
        'last_name': [1, 50],
        'age': [1, 3],
        'email': [1, 200],
        'tel': [10, 12],
        'gender': [1, 1],

        'require': ['username', 'password', 'email', 'gender']
    }

    ERROR_ARR = {}
    keys_result = list(map(str, result.keys()))

    for i in keys_result:
        if i == 'username':
            res = re.match(r'[\w0-9]+', result['username'][0])
            if not (res is not None
                    and len(res.group(0)) == len(result['username'][0])
                    and RFS['username'][0] <= len(res.group(0)) <= RFS['username'][1]):
                ERROR_ARR[
                    'Login'] = f'The Login field must be filled in, must not contain spaces or special characters, and must be at least {RFS["username"][0]} characters long.'

        if i == 'password':
            res = result['password'][0]
            if not (res is not None
                    and RFS['password'][0] <= len(res) <= RFS['password'][1]):
                ERROR_ARR[
                    'Password'] = f'The Password field must be filled in and must be at least {RFS["password"][0]} characters long.'

        if i == 'first_name':
            res = re.match(r'\w+', result['first_name'][0])
            if not (res is not None
                    and len(res.group(0)) == len(result['first_name'][0])
                    and RFS['first_name'][0] <= len(res.group(0)) <= RFS['first_name'][1]):
                ERROR_ARR[
                    'First name'] = f'The First name field must be filled in, must not contain spaces, special characters and numbers, and must be at least {RFS["first_name"][0]} characters long.'

        if i == 'last_name':
            res = re.match(r'\w+', result['last_name'][0])
            if not (res is not None
                    and len(res.group(0)) == len(result['last_name'][0])
                    and RFS['last_name'][0] <= len(res.group(0)) <= RFS['last_name'][1]):
                ERROR_ARR[
                    'Last name'] = f'The Last name field must be filled in, must not contain spaces, special characters and numbers, and must be at least {RFS["last_name"][0]} characters long.'

        if i == 'age':
            res = re.match(r'[0-9]+', result['age'][0])
            if not (res is not None
                    and len(res.group(0)) == len(result['age'][0])
                    and RFS['age'][0] <= len(res.group(0)) <= RFS['age'][1]):
                ERROR_ARR[
                    'Age'] = f'The Age field must be filled in, must contain no more than three digits.'

        if i == 'email':
            if not EMAIL_validator(result['email'][0], RFS['email'][0], RFS['email'][1]):
                ERROR_ARR[
                    'Email'] = f'The Email field must be filled in, must have the type ***@***.***'

        if i == 'tel':
            res = re.match(r'[+]?[(]?[0-9]{3}[)]?[-\s.]?[0-9]{3}[-\s.]?[0-9]{4,6}', result['tel'][0])
            if not (res is not None
                    and len(res.group(0)) == len(result['tel'][0])
                    and RFS['tel'][0] <= len(res.group(0)) <= RFS['tel'][1]):
                ERROR_ARR['Tel'] = f'The Tel field must be filled in'

        if i == 'gender':
            res = result['gender'][0]
            if not (res is not None
                    and len(res) == len(result['gender'][0])
                    and RFS['gender'][0] <= len(res) <= RFS['gender'][1]):
                ERROR_ARR['Gender'] = f'The Gender field must be filled in'

    return ERROR_ARR


def EMAIL_validator(email: str, min_len: int = 1, max_len: int = 200) -> bool:
    res = re.match(r'[A-Z0-9a-z]+@+[A-Z0-9a-z]+[.]+[A-Z0-9a-z]+', email)
    if (res is not None and
            len(res.group(0)) == len(email) and
            min_len <= len(res.group(0)) <= max_len):
        return True
    else:
        return False


def TEL_validator(tel: str, min_len: int = 11, max_len: int = 12) -> bool:
    res = re.match(r'[+]?[(]?[0-9]{3}[)]?[-\s.]?[0-9]{3}[-\s.]?[0-9]{4,6}', tel)
    if (res is not None and
            len(res.group(0)) == len(tel) and
            min_len <= len(res.group(0)) <= max_len):
        return True
    else:
        return False


def add_license_time(username, product, seconds):
    user_ = User.objects.get(username=username)
    product_ = Products.objects.get(name=product)
    if Licenses.objects.filter(username=user_, product=product_).exists():
        license_ = Licenses.objects.get(username=user_, product=product_)
        if license_.date_end > datetime.utcnow():
            license_.date_end = license_.date_end + timedelta(seconds=seconds)
        else:
            license_.date_end = datetime.utcnow() + timedelta(seconds=seconds)
    else:
        license_ = Licenses.objects.create(username=user_, product=product_)
        license_.date_end = datetime.utcnow() + timedelta(seconds=seconds)
    license_.save()


def reCAPTCHA_validation(request):
    recaptcha_response = request.POST.get('g-recaptcha-response')
    url = 'https://www.google.com/recaptcha/api/siteverify'
    values = {
        'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    }
    data = urllib.parse.urlencode(values).encode()
    req = urllib.request.Request(url, data=data)
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode())
    return result


def log(STRING: str):
    path = str(settings.BASE_DIR).replace("\\", '/') + '/log.txt'
    with open(path, 'a', encoding='utf-8') as file:
        date = str(datetime.now()) + " "
        file.write(date + STRING + '\n')


def clearing_private_msg():
    directory = settings.MEDIA_ROOT + '\\files' + '\\private_msg\\'
    files = os.listdir(directory)
    for file in files:
        if not PrivateMsg.objects.filter(file='files' + '/private_msg/' + file).exists():
            os.remove(directory + file)
        else:
            date_for_del = PrivateMsg.objects.get(file='files' + '/private_msg/' + file).date_for_del
            date_now = datetime.now()
            if date_now > date_for_del:
                os.remove(directory + file)
                PrivateMsg.objects.get(file='files' + '/private_msg/' + file).delete()

    PrivateMsgs = PrivateMsg.objects.all().values()
    for msg in PrivateMsgs:
        if datetime.now() > msg['date_for_del']:
            PrivateMsg.objects.get(key=msg['key']).delete()
