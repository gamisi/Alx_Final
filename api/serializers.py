from django.contrib.auth import get_user_model
from accounts.models import CustomUser
from garage.models import Vehicle
from rest_framework import serializers
from rest_framework.authtoken.models import Token

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields =  ['id', 'username', 'first_name', 'last_name', 'email', 'password']

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    # confirm_password = serializers.CharField()

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['key']

class VehicleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehicle
        fields = ['id', 'reg_no', 'owner', 'model', 'make', 'year']