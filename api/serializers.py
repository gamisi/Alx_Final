from django.contrib.auth import get_user_model
from accounts.models import CustomUser
from garage.models import Vehicle, Make, Model, Technician, Appointment, Maintenance, MaintenanceType, Repair, Notification
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.core.exceptions import ValidationError
import logging
from rest_framework.response import Response
from django.utils import timezone
from rest_framework import status

class CustomUserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=False, style={'input_type': 'password'})    
    confirm_password = serializers.CharField(write_only=True, required=False, style={'input_type': 'password'})
    username = serializers.CharField(read_only=True)
        
    class Meta:
        model = CustomUser
        fields =  ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'confirm_password', 'role', 'is_active']

        extra_kwargs = {

            'password': {'write_only': True},
            'confirm_password': {'write_only': True},
        }

    def generate_username(self, first_name, last_name):

        #Method to Genarate username
        username = f"{first_name.lower()}.{last_name.lower()}"
        current_username = username
        counter = 1

        while CustomUser.objects.filter(username=username).exists():
            username = f"{current_username}{counter}"
            counter += 1
        
        return username
    
    # method validates email
    def validate_email(self, value):

        user_id = self.instance.id if self.instance else None #get user id, if instance exists.
        existing_user = CustomUser.objects.filter(email=value)

        if user_id: #if this is an update exclude.
            existing_user = existing_user.exclude(id=user_id) #exclude the current user.

        if existing_user.exists():
            raise serializers.ValidationError("This email is already taken.")
        return value
    
    # create method for a new user 
    def create(self, validated_data):
        password = validated_data.pop('password')
        confirm_password = validated_data.pop('confirm_password')

        # Validate password fields to make sure they are not empty on user creation
        if password or confirm_password:
            if not password:
                raise serializers.ValidationError({"password": "Password is required."})
            if not confirm_password:
                raise serializers.ValidationError({"confirm_password": "Confirm password is required."})
            if password != confirm_password:
                raise serializers.ValidationError({"confirm_password": "password and confirm must match."})

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
        # first_name = validated_data.get('first_name')
        # last_name = validated_data.get('last_name')
        # validated_data['username'] = self.generate_username(first_name, last_name)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        if password:
            if password == confirm_password: 
                instance.set_password(password)
            else:
                raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        
        instance.save()
        return instance
               
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['key']

class VehicleSerializer(serializers.ModelSerializer):

    """owner_name = serializers.SerializerMethodField()
    model_name = serializers.SerializerMethodField()
    make_name = serializers.SerializerMethodField()"""

    class Meta:
        model = Vehicle
        fields = ['id', 'reg_no', 'year', 'owner', 'make', 'model']
        
    """def get_owner_name(self, obj):
        if obj.owner:
            return f"{obj.owner.first_name} {obj.owner.last_name}"
        return None
    
    def get_make_name(self, obj):
        if obj.make:
            return f"{obj.make.make_name}"
        return None

    def get_model_name(self, obj):
        if obj.model:
            return f"{obj.model.model_name}"
        return None"""
    
    #validate owner.
    def validate_owner(self, value): 
        if value is None:
            raise serializers.ValidationError("Owner is required.")
        return value
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context.get('request').user 

        if user.role and user.role.role_name == 'customer': 
            self.fields['owner'].queryset = CustomUser.objects.filter(id=user.id)             
        else:
            self.fields['owner'].queryset = CustomUser.objects.all()

class MakeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Make
        fields = ['id', 'make_name', 'make_desc']

class ModelSerializer(serializers.ModelSerializer):

    class Meta: 
        model = Model
        fields = ['id', 'model_name', 'model_desc']

class TechnicianSerializer(serializers.ModelSerializer):

    class Meta:
        model = Technician
        fields = ['id', 'name','phone_no','specialty']

class AppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = ['id', 'vehicle_id', 'appointment_date', 'description']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context.get('request').user 

        if user.role and user.role.role_name == 'customer': 

            self.fields['vehicle_id'].queryset = Vehicle.objects.filter(owner=user)             
        else:
            self.fields['vehicle_id'].queryset = Vehicle.objects.all() 
    
    def validate(self, data):

        appointment_date = data.get('appointment_date')
        vehicle = data.get('vehicle_id')

        if appointment_date and appointment_date < timezone.now():
            raise ValidationError({"appointment_date": "Appointment date cannot be in the past."})

        if vehicle and Appointment.objects.filter(vehicle_id=vehicle, status='open').exists(): 
            raise ValidationError({"vehicle_id": "This vehicle already has an open appointment. Please contact admin for further assistance"})

        return data


class MaintenanceSerializer(serializers.ModelSerializer):

    total_cost = serializers.CharField(read_only=True)
    cost = serializers.CharField(read_only=True)

    class Meta:
        model = Maintenance
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = ['id', 'user_id', 'message', 'nofitication_date', 'notification_type']

class RepairSerializer(serializers.ModelSerializer):
    
    # vehicle_id = serializers.StringRelatedField(read_only=True)
    # mechanic = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Repair
        fields = ['id', 'vehicle_id', 'mechanic','repair_date', 'repair_cost', 'description']

class MaintenanceTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = MaintenanceType
        fields = ['id', 'maintenance_type_name', 'maintenance_type_cost']