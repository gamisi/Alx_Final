from django.contrib.auth import get_user_model
from .models import CustomUser
from rest_framework import serializers
from rest_framework.authtoken.models import Token

class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields =  ['id', 'username', 'first_name', 'last_name', 'email', 'password']

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['key']


