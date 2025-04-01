from .import views
from django.urls import path
from .views import VehicleListView, AddVehicleView

urlpatterns = [
        
        path('vehicles/', VehicleListView.as_view(), name='all_vehicles'),
        path('api/vehicles/', views.get_vehicles, name='vehicles'),  
        path('add_vehicle/', AddVehicleView.as_view(), name="add_vehicle"),
        path('edit_vehicle/<int:pk>/', AddVehicleView.as_view(), name="edit_vehicle"),   
        path('delete-vehicle/<int:pk>/', views.delete_vehicle, name='delete_vehicle')     

]