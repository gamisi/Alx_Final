from django.urls import path, include
from .views import UserViewset, VehicleViewSet, MakeViewSet, ModelViewSet, APIRoot, TechnicianViewSet, AppointmentsViewSet, MaintenanceViewSet, NotificationsViewSet, RepairViewSet, MaintenanceTypeViewSets, UserListView, VehicleListView, UserDetailView, UserCreateView, UserUpdateView
from rest_framework.routers import DefaultRouter
from . import views

#Create router here and register the viewsets
router = DefaultRouter()
router.register(r'users', UserViewset, basename='users')
router.register(r'vehicles', VehicleViewSet, basename='vehicles')
router.register(r'make', MakeViewSet, basename='make')
router.register(r'model', ModelViewSet, basename='model')
router.register(r'technicians', TechnicianViewSet, basename='technicians')
router.register(r'appointments',AppointmentsViewSet, basename="appointments")
router.register(r'maintenance', MaintenanceViewSet, basename='maintenance')
router.register(r'notifications', NotificationsViewSet, basename='notifications')
router.register(r'maintenancetypes', MaintenanceTypeViewSets, basename='maintenancetypes')
router.register(r'repairs', RepairViewSet, basename="repairs")


app_name = 'api'

urlpatterns = [

    path('',APIRoot.as_view(), name='api-root'),
    path('apis/', include(router.urls)),

    #users
    path('users/', UserListView.as_view(), name='user-list' ),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail' ),
    path('users/create/', UserCreateView.as_view(), name='user-create' ),
    path('users/update/<int:pk>/', UserUpdateView.as_view(), name='user-update' ),
    path('users/delete/<int:pk>/', views.UserDeleteView.as_view(), name='user-delete'),

    #vehicles
    path('vehicles/', VehicleListView.as_view(), name='vehicle-list' ),

    
]