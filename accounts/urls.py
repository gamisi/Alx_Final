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

    path('', redirect_to_login, name='home'),
    path('api/login', UserLoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    # path('dashboard/', views.DashboardView, name='dashboard'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('logout/', custom_logout, name='logout'),
    # path('api/', include(router.urls)),

]