from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CustomUser


class RegistrationForm(UserCreationForm):

    email = forms.EmailField(required=True)
    first_name = forms.Field(required=True)
    last_name = forms.Field(required=True)
    
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None  
    
    def generate_username(self, first_name, last_name):

        #Method Genarate base username
        username = f"{first_name.lower()}.{last_name.lower()}"
        current_username = username
        counter = 1

        while CustomUser.objects.filter(username=username).exists():
            username = f"{current_username}{counter}"
            counter += 1
        
        return username
    
    def save(self, commit=True):
        
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password1']

        username = self.generate_username(first_name, last_name)

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        return user