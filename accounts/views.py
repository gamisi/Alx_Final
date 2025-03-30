from django.shortcuts import render
from rest_framework import generics, viewsets
from .serializers import CustomUserSerializer, UserLoginSerializer
from .models import CustomUser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .forms import RegistrationForm
from django.contrib.auth import login, logout , authenticate
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib.auth.forms import PasswordResetForm
import os


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

    # Pass the logged-in user to the template
    """def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user  
        return context"""

"""def password_reset(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
    else:
        form = CustomPasswordResetForm()

    return render (request, 'registration/password_reset_form.html', {"form": form})"""

class CustomPasswordResetView(PasswordResetView):
    form_class = PasswordResetForm
    template_name = 'registration/password_reset.html'

    def dispatch(self, request, *args, **kwargs):
        print(self.form_class) #add this print statement.
        return super().dispatch(request, *args, **kwargs)




