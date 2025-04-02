from .import views
from django.urls import path
from .views import VehicleListView, AddVehicleView, MakeView, ModelView, AddMakeView, AddModelView, TechnicianView, AddMechanicView

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
        path('technicians/', TechnicianView.as_view(), name='all_mechanics'),
        path('api/technicians/', views.get_technicians, name='mechanics'),
        path('add_mechanic/', AddMechanicView.as_view(), name="add_mechanic"),
        path('edit_mechanic/<int:pk>/', AddMechanicView.as_view(), name="edit_mechanic"),
        path('delete-mechanic/<int:pk>/', views.delete_mechanic, name='delete_mechanic'),
]