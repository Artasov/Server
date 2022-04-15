from rest_framework.serializers import ModelSerializer
from APP_home.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
