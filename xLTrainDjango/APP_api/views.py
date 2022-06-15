import json
from datetime import datetime

from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.views import APIView

from APP_home.models import User
from APP_shop.models import Products, Licenses
from params_and_funcs import log
from xLTrainDjango.xLLIB_v1 import random_str
from .serializers import UserSerializer


class UserAPIView(APIView):
    permission_classes = (IsAdminUser,)
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get(self, request):
        all_users = User.objects.all()
        return Response({'users': UserSerializer(all_users, many=True).data})


class UserAPIViewByName(APIView):
    permission_classes = (IsAdminUser,)
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get(self, request, name):
        user = User.objects.filter(username=name)

        if len(user) == 0:
            return Response({'error': f'User with name {name} does not exist'})

        return Response({name: UserSerializer(user, many=True).data})


@api_view(['GET'])
def RandomStrAPIView(request):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    params = dict(request.GET)

    try:
        try:
            count = int(params['count'][0])
            length = int(params['length'][0])
            alphabet = params['alphabet'][0]
            repete = True if params['repete'][0] == 'True' or params['repete'][0] == 'true' else False
            upper = True if params['upper'][0] == 'True' or params['upper'][0] == 'true' else False
            digits = True if params['digits'][0] == 'True' or params['digits'][0] == 'true' else False
        except ValueError:
            return Response({
                "response": 'ERROR. Check if the request belongs to a template: http://xxx.xx/random_str?length=int&alphabet=x&repete=bool&upper=bool&digits=bool. For more information, see the documentation on the xlartas website.'})

        if length > 400:
            return Response({
                "response": 'length value must be less than 400. For more information, see the documentation on the xlartas website.'})
        if count > 200:
            return Response({
                "response": 'count value must be less than 200. For more information, see the documentation on the xlartas website.'})
        if len(alphabet) > 200:
            return Response({
                "response": 'alphabet value length must be less than 200. For more information, see the documentation on the xlartas website.'})

        rand_strs_list = []

        for i in range(count):
            rand_strs_list.append(random_str(
                length=length,
                alphabet=alphabet,
                repete=repete,
                upper=upper,
                digits=digits
            ))
    except KeyError:
        return Response({
            "response": 'ERROR. Check if the request belongs to a template: http://xxx.xx/random_str?length=int&alphabet=x&repete=bool&upper=bool&digits=bool. For more information, see the documentation on the xlartas website.'})

    return Response({"response": rand_strs_list})


@csrf_exempt
@api_view(['POST'])
def ProgramAuth(request):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    if request.method == "POST":
        json_date = list(dict(request.POST).keys())[0]
        data = dict(json.loads(json_date))
        user = authenticate(request, username=data['username'], password=data['password'])
        if user is not None:
            FIRST = False
            user = User.objects.get(username=data['username'])
            if user.HWID is None:
                user.HWID = data['HWID']
                user.save()
                FIRST = True
            else:
                if data['HWID'] != user.HWID:
                    return Response({'accept': False, 'error': 'HWID_ERR'},
                                    headers={'Content-Type': 'application/json'})

            product = Products.objects.get(name=data['product'])
            user_license = Licenses.objects.filter(username=user, product=product)
            DATE_LICENSE = user_license.first().date_end
            DATE_NOW = datetime.utcnow()
            if DATE_LICENSE > DATE_NOW:
                return Response({'accept': True, 'HWID': user.HWID, 'FIRST': FIRST},
                                headers={'Content-Type': 'application/json'})

            return Response({'accept': False, 'error': 'License timeout'},
                            headers={'Content-Type': 'application/json'})
        else:
            return Response({'accept': False, 'error': 'Login or password\n invalid'},
                            headers={'Content-Type': 'application/json'})
    else:
        return Response({'accept': False, 'error': 'Invalid request'}, headers={'Content-Type': 'application/json'})


@csrf_exempt
@api_view(['POST'])
def SetHWID(request):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    if request.method == "POST":
        json_date = list(dict(request.POST).keys())[0]
        data = dict(json.loads(json_date))
        user = authenticate(request, username=data['username'], password=data['password'])
        if user is not None:
            user = User.objects.get(username=data['username'])

            user.HWID = data['HWID']
            user_licenses = Licenses.objects.filter(username=user)
            for license_ in user_licenses:
                license_.date_end = datetime.utcnow()
                license_.save()
            user.save()
            return Response({'accept': True, },
                            headers={'Content-Type': 'application/json'})

        else:
            return Response({'accept': False, 'error': 'Login or pass invalidы'},
                            headers={'Content-Type': 'application/json'})
    else:
        return Response({'accept': False, 'error': 'Something go wrong'}, headers={'Content-Type': 'application/json'})


@api_view(['GET'])
def ProductVersion(request, product):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    if Products.objects.filter(name=product).exists():
        product = Products.objects.get(name=product)
        return Response({'version': product.version}, headers={'Content-Type': 'application/json'})
    else:
        return Response('Product does not exist.', headers={'Content-Type': 'application/json'})
