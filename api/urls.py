from django.urls import path, include
from .views import UserViewset, VehicleViewSet
from rest_framework.routers import DefaultRouter

#Create router here and register the viewsets
router = DefaultRouter()
router.register(r'users', UserViewset, basename='users')
router.register(r'vehicles', VehicleViewSet, basename='vehicles')

urlpatterns = [

    path('', include(router.urls)),
    
]