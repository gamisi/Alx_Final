from django.contrib.auth import get_user_model
from accounts.models import CustomUser
from garage.models import Vehicle, Make, Model, Technician
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

class MakeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Make
        fields = ['id', 'make_name', 'make_desc']

class ModelSerializer(serializers.ModelSerializer):

    class Meta: 
        model = Model
        fields = ['id', 'model_name', 'model_desc']