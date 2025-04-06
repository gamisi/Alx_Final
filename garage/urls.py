from .import views
from django.urls import path
from .views import VehicleListView, AddVehicleView, MakeView, ModelView, AddMakeView, AddModelView, MechanicView, AddMechanicView, MaintenanceTypeView, AddMaintenancetypeView, MaintenanceView, AddMaintenanceView, RepairsView, AddRepairsView, AppointmentView, AddAppoitnmentView

urlpatterns = [
        
        #vehicles
        path('vehicles/', VehicleListView.as_view(), name='all_vehicles'),
        path('api/vehicles/', views.get_vehicles, name='vehicles'),  
        path('add_vehicle/', AddVehicleView.as_view(), name="add_vehicle"),
        path('edit_vehicle/<int:pk>/', AddVehicleView.as_view(), name="edit_vehicle"),   
        path('delete-vehicle/<int:pk>/', views.delete_vehicle, name='delete_vehicle'),    

        #Makes
        path('makes/', MakeView.as_view(),  name='all_makes'),
        path('api/makes/', views.get_makes, name='makes'),
        path('add_make/', AddMakeView.as_view(), name="add_make"),
        path('edit_make/<int:pk>/', AddMakeView.as_view(), name="edit_make"),
        path('delete-make/<int:pk>/', views.delete_make, name='delete_make'),

        #models
        path('models/', ModelView.as_view(),  name='all_models'),
        path('api/models/', views.get_models, name='models'),
        path('add_model/', AddModelView.as_view(), name="add_model"),        
        path('edit_model/<int:pk>/', AddModelView.as_view(), name="edit_model"),
        path('delete-model/<int:pk>/', views.delete_model, name='delete_model'),

        #mechanics
        path('technicians/', MechanicView.as_view(), name='all_mechanics'),
        path('api/technicians/', views.get_technicians, name='mechanics'),
        path('add_mechanic/', AddMechanicView.as_view(), name="add_mechanic"),
        path('edit_mechanic/<int:pk>/', AddMechanicView.as_view(), name="edit_mechanic"),
        path('delete-mechanic/<int:pk>/', views.delete_mechanic, name='delete_mechanic'),

        #maintenance 
        path('maintenancetypes/', MaintenanceTypeView.as_view(), name='maintenance_types'),
        path('api/maintenancetypes/', views.get_maintenance_types, name='api_maintenance_types'),
        path('add_maintenancetype/', AddMaintenancetypeView.as_view(), name='add_maintenance_type'),
        path('edit_maintenancetype/<int:pk>/', AddMaintenancetypeView.as_view(), name='edit_maintenance_type'),
        path('delete_maintenancetype/<int:pk>/', views.delete_maintenance_type, name='delete_maintenance_type'),

        path('maintenances/', MaintenanceView.as_view(), name='all_maintenances'),
        path('api/maintenances/', views.get_maintenances, name='maintenances'),
        path('add_maintenance/', AddMaintenanceView.as_view(), name='add_maintenance'),
        path('edit_maintenance/<int:pk>/', AddMaintenanceView.as_view(), name='edit_maintenance'),
        path('delete-maintenance/<int:pk>/', views.delete_maintenance, name='delete_maintenance'),

        #repairs
        path('repairs/', RepairsView.as_view(), name='all_repairs'),
        path('add_repair/', AddRepairsView.as_view(), name='add_repair'),
        path('api/all_repairs/', views.get_repairs, name='get_repairs'),
        path('edit_repair/<int:pk>/', AddRepairsView.as_view(), name='edit_repair'),
        path('delete-repair/<int:pk>/', views.delete_repair, name='delete_repair'),

        #Appointments
        path('appointments/', AppointmentView.as_view(), name='all_appointments' ),
        path('api/appointments/', views.get_appointments, name="get_appointments"),
        path('add_appointment/', AddAppoitnmentView.as_view(), name='add_appointment'),
        path('edit_appointment/<int:pk>/', AddAppoitnmentView.as_view(), name='edit_appointment'),
        path('delete-appointment/<int:pk>/', views.delete_appointment, name='delete_appointment'),       
]