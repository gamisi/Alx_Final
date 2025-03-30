from django.urls import path, include
from .views import UserViewset
from .views import UserLoginView, DashboardView
from rest_framework.routers import DefaultRouter
from .import views
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from .views import custom_logout

#Create router here and register the viewsets
router = DefaultRouter()
router.register(r'users', UserViewset, basename='users')

def redirect_to_login(request):
    return redirect('login')

urlpatterns =  [

    path('', redirect_to_login, name='/login'),
    path('api/login', UserLoginView.as_view(), name='login'),
    # path('register/', views.register, name='register'),
    path('accounts/dashboard/', DashboardView.as_view(), name='dashboard'),
    path('logout/', custom_logout, name='logout'),
    path('accounts/sign-up/', views.sign_up, name='sign_up'),
    #path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/', views.custom_password_reset, name='password_reset'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
]