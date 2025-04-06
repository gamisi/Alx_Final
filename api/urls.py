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

    # path('',APIRoot.as_view(), name='api-root'),
    path('apis/', include(router.urls)),
    
    #users
    path('users/', UserListView.as_view(), name='user-list' ),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail' ),
    path('users/create/', UserCreateView.as_view(), name='user-create' ),
    path('users/update/<int:pk>/', UserUpdateView.as_view(), name='user-update' ),
    path('users/delete/<int:pk>/', views.UserDeleteView.as_view(), name='user-delete'),
    path('users/login/', views.ApiLoginView.as_view(), name='login'),

    #vehicles
    path('vehicles/', VehicleListView.as_view(), name='vehicle-list' ),
    path('vehicles/create/', views.VehicleCreateView.as_view(), name='vehicle-create'),
    path('vehicles/<int:pk>/', views.VehicleDetailView.as_view(), name='vehicle-detail' ),
    path('vehicles/update/<int:pk>/', views.VehicleUpdateView.as_view(), name='vehicle-update' ),
    path('vehicles/delete/<int:pk>/', views.VehicleDeleteView.as_view(), name='vehicle-delete'),

    #makes 
    path('makes/', views.MakeListView.as_view(), name='make-list'),
    path('makes/create/', views.MakeCreateView.as_view(), name='make-create'),
    path('makes/<int:pk>/', views.MakeDetailView.as_view(), name='makes-detail'),
    path('makes/update/<int:pk>/', views.MakeUpdateView.as_view(), name='make-update'),
    path('makes/delete/<int:pk>/', views.MakeDeleteView.as_view(), name='make-delete'),

    #makes 
    path('models/', views.ModelListView.as_view(), name='model-list'),
    path('models/create/', views.ModelCreateView.as_view(), name='model-create'),
    path('models/<int:pk>/', views.ModelDetailView.as_view(), name='model-detail'),
    path('models/update/<int:pk>/', views.ModelUpdateView.as_view(), name='model-update'),
    path('models/delete/<int:pk>/', views.ModelDeleteView.as_view(), name='model-delete'),

    #mechanic
    path('mechanics/', views.MechanicListView.as_view(), name='mechanic-list'),
    path('mechanics/create/', views.MechanicCreateView.as_view(), name='mechanic-create'),
    path('mechanics/<int:pk>/', views.MechanicDetailView.as_view(), name='mechanic-detail'),
    path('mechanics/update/<int:pk>/', views.MechanicUpdateView.as_view(), name='mechanic-update'),  
    path('mechanics/delete/<int:pk>/', views.DeleteMechanicView.as_view(), name='mechanic-delete'),  

    #maintenance
    path('maintenances/', views.MaintenanceListView.as_view(), name='maintenance-list'),
    path('maintenances/create/', views.MaintenanceCreateView.as_view(), name='maintenance-create'),
    path('maintenances/<int:pk>/', views.MaintenanceDetailView.as_view(), name='maintenance-detail'),
    path('maintenances/update/<int:pk>/', views.MaintenanceUpdateView.as_view(), name="maintenance-update"),
    path('maintenances/delete/<int:pk>/', views.MaintenanceDeleteView.as_view(), name='maintenance-delete'),

    #repairs
    path('repairs/', views.RepairsListView.as_view(), name='repairs-list'),
    path('repairs/<int:pk>/', views.RepairsDetailView.as_view(), name='repair-detail'),
    path('repairs/create/', views.RepairsCreateView.as_view(), name='repair-create'),
    path('repairs/update/<int:pk>/', views.RepairsUpdateView.as_view(), name='update-repairs'),
    path('repairs/delete/<int:pk>/', views.RepairDeleteView.as_view(), name='delete-view'),

    #appointments
    path('appointments/', views.AppointmentListView.as_view(), name='appointment-list'),
    path('appointments/<int:pk>/', views.AppointmentDetailView.as_view(), name="appointment-detail"),
    path('appointments/create/', views.AppointmentCreateView.as_view(), name='appointment-create'),
    path('appointments/update/<int:pk>/', views.AppointmentsUpdateView.as_view(), name="appointment-update"),
    path('appointments/delete/<int:pk>/', views.AppointmentsDeleteView.as_view(), name='appointment-delete')

]