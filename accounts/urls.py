from django.urls import path, include
from .views import UserViewset
from .views import UserLoginView
from rest_framework.routers import DefaultRouter
from .import views


#Create router here and register the viewsets
router = DefaultRouter()
router.register(r'users', UserViewset, basename='users')

urlpatterns =  [

    path('', views.home, name='home'),
    path('api/login', UserLoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),

    # API Routes
    path('api/', include(router.urls)),

]