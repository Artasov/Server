from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.views import APIView

from APP_home.models import User
from xLTrainDjango.xLLIB_v1 import random_str
from .serializers import UserSerializer


class UserAPIView(APIView):
    permission_classes = (IsAdminUser,)
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get(self, request):
        print(1)
        all_users = User.objects.all()
        print(2)
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
def RekrutoTask(request):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    params = dict(request.GET)
    # return Response({'response': f'Hello {params["name"][0]}! {params["message"][0]}'})
    return HttpResponse(f'Hello {params["name"][0]}!<br>{params["message"][0]}')


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
