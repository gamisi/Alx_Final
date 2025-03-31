from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets
from .serializers import CustomUserSerializer, UserLoginSerializer
from .models import CustomUser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.contrib.auth import logout, authenticate
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DetailView
from .forms import RegistrationForm, CustomSetPasswordForm, UserEditForm
from django.contrib.auth import login, logout , authenticate
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.forms import PasswordResetForm
from django.db.models import F,CharField, Value
from django.db.models.functions import Concat
from django.utils.html import format_html
import os
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

# Create your views here.
class UserViewset(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class UserLoginView(APIView):
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'here is your token': {token.key}}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
def register(request):
    return render(request, 'registration/register.html')

def login (request):
    page_title = os.path.splitext(os.path.basename('registration/sign_up.html'))[0].capitalize()
    context = {

        'page_title': page_title,
    }
    return render(request, 'registration/login.html', context)
"""
def custom_logout(request):
    logout(request)  # This will log the user out
    return redirect(reverse('login'))  # Redirect to the login page

def sign_up(request):

    """page_title = os.path.splitext(os.path.basename('registration/sign_up.html'))[0].capitalize()
    context = {

        'page_title': page_title,
    }"""

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            #login(request, user)
            return redirect('/sign-up')
    else:
        form = RegistrationForm()
            
    return render(request,'registration/sign_up.html', {"form": form})

"""
#Function Based View
@login_required
def DashboardView(request):
    return render(request, 'accounts/dashboard.html')
"""

#class based view
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'
    login_url =  '/login/'


"""def password_reset(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
    else:
        form = CustomPasswordResetForm()

    return render (request, 'registration/password_reset_form.html', {"form": form})"""

"""class CustomPasswordResetView(PasswordResetView):
    form_class = PasswordResetForm
    template_name = 'registration/password_reset.html'"""


def custom_password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            # Send password reset email
            email = form.cleaned_data['email']
            users = CustomUser.objects.filter(email=email)
            for user in users:
                
                # generate reset token and send email
                token = default_token_generator.make_token(user)
                uidb64 = urlsafe_base64_encode(str(user.pk).encode())
                
                # debugging
                """print(f"Generated uidb64: {uidb64}")  
                print(f"Generated token: {token}")"""    

                reset_url = f"http://{get_current_site(request).domain}/reset/{uidb64}/{token}/"

                                
                email_subject = "Password Reset Request"
                email_body = render_to_string('registration/password_email.html', {
                    
                    'reset_url': reset_url,
                    'user': user,
                })
        
                send_mail(
                    
                    email_subject, 
                    email_body, 
                    settings.DEFAULT_FROM_EMAIL, [email],
                    html_message=email_body,
                )
                
            return redirect('password_reset_done')
    else:
        form = PasswordResetForm()

    return render(request, 'registration/password_reset.html', {'form': form})

class SetCustomPasswordView(PasswordResetConfirmView):
    template_name='registration/password_confirm.html' 
    form_class=CustomSetPasswordForm

class UserListView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/users-list.html'
    login_url = '/login/'

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users(request):
    users = CustomUser.objects.annotate(
        #concat first name and last name
        full_name=Concat(
            F('first_name'), Value(' '), F('last_name'),
            output_field=CharField()
        )

    ).values(
        
        # fields that should be selected form the users table
        'id', 'username', 'email', 'full_name', 'role'
    )
    data = []
    for index, user in enumerate(users):
        data.append({

            'rowIndex': index + 1,
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'full_name': user['full_name'],
            'role_name': user['role'],
            'actions': format_html(

                '<div class="btn-group">'
                    '<button class="btn btn-sm btn-info ml-1" title="view user info" data-id="{}" id="editUserBtn" data-toggle="modal" data-target="#updateUserModal">'
                        '<i class="fa fa-eye" aria-hidden="true"></i>'
                    '</button>'
                    '<button class="btn btn-sm btn-primary ml-1" title="change password" data-id="{}" id="viewUserBtn" data-toggle="modal" data-target="#viewUserModal">'
                        '<i class="fa fa-lock" aria-hidden="true"></i>'
                    '</button>'
                    '<button class="btn btn-sm btn-danger ml-1" title="delete user" data-id="{}" id="deleteUserBtn">'
                        '<i class="fa fa-trash" aria-hidden="true"></i>'
                    '</button>'
                '</div>',

                user['id'], user['id'], user['id']
            ),
            'checkbox': format_html(

                '<input type="checkbox" name="role_checkbox" data-id="{}"><label></label>',
                user['id']

            ),
        })

    return Response(data)

class UserDetailView(LoginRequiredMixin, TemplateView):
    form_class = UserEditForm
    template_name = 'accounts/view_user.html'  
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(CustomUser, pk=kwargs['pk'])
        form = UserEditForm(instance=user)
        context['form'] = form
        context['user'] = user
        return context

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    pass
    
