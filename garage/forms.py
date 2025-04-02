from django import forms
from accounts.models import CustomUser
from .models import Vehicle, Make, Model, Technician, Repair, Maintenance, MaintenanceType, Appointment, Notification
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, HTML

class AddVehicleForm(forms.ModelForm):    
    
    class Meta:
        model = Vehicle
        fields =('reg_no','owner', 'model', 'make', 'year')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.field_class = 'filtered-select'
        self.helper.layout = Layout(

            Field('model', css_class='filtered-select')

        )

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

    class Meta:
        form = Repair
        fields = ()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class MaintenanceForm(forms.ModelForm):

    class Meta:
        form = Maintenance
        fields = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class MaintenanceTypeForm(forms.ModelForm):

    class Meta:
        model = MaintenanceType
        fields = ('maintenance_type_name', 'maintenance_type_cost', 'maintenance_type_desc')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class AppointmentForm(forms.ModelForm):

    class Meta:
        form = Appointment
        fields = ()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class NotificationForm(forms.ModelForm):

    class Meta:
        form = Notification
        fields = ()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)