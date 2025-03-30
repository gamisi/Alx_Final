from django.urls import path, include
from .views import UserViewset
from .views import UserLoginView, DashboardView, SetCustomPasswordView, UserListView
from rest_framework.routers import DefaultRouter
from .import views
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from .forms import CustomSetPasswordForm

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
    path('logout/', views.custom_logout, name='logout'),
    path('accounts/sign-up/', views.sign_up, name='sign_up'),
    #path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/', views.custom_password_reset, name='password_reset'),
    path('reset/<uidb64>/<token>/', SetCustomPasswordView.as_view(), name='password_reset_confirm'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/reset_complete.html'), name="password_reset_complete"),

    #user management urls
    path('accounts/user-list', UserListView.as_view(), name='user_list'),
    path('api/users/', views.get_users, name='get_users'),

]