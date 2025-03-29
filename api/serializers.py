from django.contrib.auth import get_user_model
from accounts.models import CustomUser
from garage.models import Vehicle, Make, Model, Technician
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.core.exceptions import ValidationError


class CustomUserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    username = serializers.CharField(read_only=True)
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields =  ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']
    
    def generate_username(self, first_name, last_name):

        #Method Genarate base username
        username = f"{first_name.lower()}.{last_name.lower()}"
        current_username = username
        counter = 1

        while CustomUser.objects.filter(username=username).exists():
            username = f"{current_username}{counter}"
            counter += 1
        
        return username
    
    def validate(self, data):

        """
        print(type(data))  # Check the type of 'data'
        print(data)        # Check what 'data' contains
        """

        password = data.get('password')
        confirm_passowrd = data.get('confirm_password')

        if password != confirm_passowrd:
            raise serializers.ValidationError({"confirm_passwords": "passwords do not match"})
        
        return data

    # method validates email
    def validate_email(self, value):
        #check if email is unique
        if CustomUser.objects.filter(email=value).exists():
            raise ValidationError("Email has already been taken")
        return value
    
    # This method ensures passowrd is hashed
    def create(self, validated_data):
        password = validated_data.pop('password')
        confirm_password = validated_data.pop('confirm_password')

        # Generate username based on first and last name
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        validated_data['username'] = self.generate_username(first_name, last_name)

        user = CustomUser.objects.create(**validated_data)
        user.set_password(password) #hash the password using PKF
        user.save()

        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        confirm_password = validated_data.pop('confirm_password', None)

        # Generate username based on first and last name
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        validated_data['username'] = self.generate_username(first_name, last_name)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance

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