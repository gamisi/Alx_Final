from django import forms
from accounts.models import CustomUser
from .models import Vehicle, Make, Model, Technician, Repair, Maintenance, MaintenanceType, Appointment, Notification
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, HTML
from django.utils import timezone
import datetime


class AddVehicleForm(forms.ModelForm):    
    
    class Meta:
        model = Vehicle
        fields =('reg_no','owner', 'model', 'make', 'year')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            #print(f"User Role: {user.role.role_name if user.role else None}")
            if user.role and user.role.role_name == 'customer':
                self.fields['owner'].queryset = CustomUser.objects.filter(id=user.id)
            else:
                self.fields['owner'].queryset = CustomUser.objects.filter(role__role_name='customer')
               
class MakeForm(forms.ModelForm):

    class Meta:
        model = Make 
        fields = ('make_name', 'make_desc')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ModelForm(forms.ModelForm):

    class Meta:
        model = Model
        fields = ('model_name', 'model_desc')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class TechnicianForm(forms.ModelForm):

    class Meta:
        model = Technician
        fields = ('name', 'phone_no', 'specialty')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class RepairForm(forms.ModelForm):

    repair_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Repair
        fields = ('vehicle_id', 'mechanic', 'repair_date', 'repair_cost', 'description')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

class MaintenanceForm(forms.ModelForm):
    
    maintenance_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Maintenance
        fields = ('vehicle_id', 'mechanic', 'maintenance_date', 'maintenance_types', 'mileage', 'cost', 'miscellaneous_cost', 'total_cost')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cost'].widget.attrs['readonly'] = True
        self.fields['total_cost'].widget.attrs['readonly'] = True
        

class MaintenanceTypeForm(forms.ModelForm):

    class Meta:
        model = MaintenanceType
        fields = ('maintenance_type_name', 'maintenance_type_cost', 'maintenance_type_desc')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class AppointmentForm(forms.ModelForm):

    #appointment_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    appointment_date = forms.DateTimeField(

        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M')

    )

    class Meta:
        model = Appointment
        fields = ('vehicle_id', 'appointment_date', 'description')
    
    def clean(self):
        cleaned_data = super().clean()
        vehicle = cleaned_data.get('vehicle_id')
        appointment_date = cleaned_data.get('appointment_date')
        instance = getattr(self, 'instance', None)
        
        if vehicle and appointment_date:
            # Check for existing open appointments, excluding the current appointment if editing.
            open_appointment = Appointment.objects.filter(vehicle_id=vehicle, status='open')

            if instance:
                open_appointment = open_appointment.exclude(pk=instance.pk) #exclude the current appointment.

            if open_appointment.exists():
                raise forms.ValidationError('Vehicle already has an open appointment please contact admin to close it before opening a new appointment.')

            if appointment_date < timezone.now():
                raise forms.ValidationError('Appointment date and time cannot be in the past.')


        return cleaned_data
    
    def __init__(self, *args, **kwargs):        
        user = kwargs.pop('user', None) 
        super().__init__(*args, **kwargs)

        if user:            
            # print(f"User Role: {user.role if hasattr(user, 'role') else None}") 
            if user.role and user.role.role_name == 'customer':
                self.fields['vehicle_id'].queryset = Vehicle.objects.filter(owner=user)
            else:
                self.fields['vehicle_id'].queryset = Vehicle.objects.all()
        

class NotificationForm(forms.ModelForm):

    class Meta:
        form = Notification
        fields = ()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)