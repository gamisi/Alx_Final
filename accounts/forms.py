from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from .models import CustomUser
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Submit

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

"""class CustomPasswordResetForm(PasswordResetForm):
    
    class Meta:
        model = CustomUser
        fields = ['email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)"""

class CustomSetPasswordForm(SetPasswordForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].help_text = None
        self.fields['new_password2'].help_text = None

class UserEditForm(forms.ModelForm):
    # role = forms.Field()
    class Meta:
        model = CustomUser
        fields = ('username','email', 'first_name', 'last_name', 'role', 'is_active', 'is_staff', 'is_superuser')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.fields['is_active'].help_text = None
        self.fields['is_staff'].help_text = None
        self.fields['is_superuser'].help_text = None

        