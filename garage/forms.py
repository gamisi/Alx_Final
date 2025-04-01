from django import forms
from accounts.models import CustomUser
from .models import Vehicle
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