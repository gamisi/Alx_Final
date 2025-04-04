from django.contrib.auth import get_user_model
from accounts.models import CustomUser
from garage.models import Vehicle, Make, Model, Technician, Appointment, Maintenance, MaintenanceType, Repair, Notification
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.core.exceptions import ValidationError


class CustomUserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(required=False)    
    confirm_password = serializers.CharField(required=False)
    username = serializers.CharField(read_only=True)
    
    class Meta:
        model = CustomUser
        fields =  ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'confirm_password', 'role', 'is_active']
    
    def generate_username(self, first_name, last_name):

        #Method to Genarate username
        username = f"{first_name.lower()}.{last_name.lower()}"
        current_username = username
        counter = 1

        while CustomUser.objects.filter(username=username).exists():
            username = f"{current_username}{counter}"
            counter += 1
        
        return username
    
    def validate(self, data):

        password = data.get('password')
        confirm_passowrd = data.get('confirm_password')

        if password != confirm_passowrd:
            raise serializers.ValidationError({"confirm_passwords": "passwords do not match"})
        
        return data

    # method validates email
    def validate_email(self, value):

        user_id = self.instance.id if self.instance else None #get user id, if instance exists.
        existing_user = CustomUser.objects.filter(email=value)

        if user_id: #if this is an update.
            existing_user = existing_user.exclude(id=user_id) #exclude the current user.

        if existing_user.exists():
            raise serializers.ValidationError("This email is already taken.")
        return value
    
    # This method ensures passowrd is hashed and username is generated    
    def create(self, validated_data):
        password = validated_data.pop('password')
        confirm_password = validated_data.pop('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})

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

    owner = serializers.SerializerMethodField()
    model = serializers.SerializerMethodField()
    make = serializers.SerializerMethodField()

    def get_owner(self, obj):
        if obj.owner:
            return f"{obj.owner.first_name} {obj.owner.last_name}"
        return None
    
    def get_make(self, obj):
        if obj.make:
            return f"{obj.make.make_name}"
        return None

    def get_model(self, obj):
        if obj.model:
            return f"{obj.model.model_name}"
        return None


    class Meta:
        model = Vehicle
        fields = '__all__'

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
        fields = ['id', 'user_id', 'vehicle_id', 'appointment_date', 'description']

class MaintenanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Maintenance
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = ['id', 'user_id', 'message', 'nofitication_date', 'notification_type']

class RepairSerializer(serializers.ModelSerializer):

    class Meta:
        model = Repair
        fields = ['id', 'vehicle_id', 'mechanic', 'repair_date', 'repair_cost', 'description']

class MaintenanceTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = MaintenanceType
        fields = ['id', 'maintenance_type_name', 'maintenance_type_cost']