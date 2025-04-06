from django.shortcuts import render
from rest_framework import generics, viewsets
from .serializers import CustomUserSerializer, UserLoginSerializer, VehicleSerializer, MakeSerializer, ModelSerializer, TechnicianSerializer, AppointmentSerializer, MaintenanceSerializer, MaintenanceTypeSerializer, NotificationSerializer, RepairSerializer
from accounts.models import CustomUser, Role
from garage.models import Vehicle, Make, Model, Technician, Appointment, Repair, Maintenance, Notification, MaintenanceType
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import redirect
from rest_framework.reverse import reverse
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import logout, authenticate
from rest_framework.authtoken.models import Token
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from django.shortcuts import get_object_or_404
from decimal import Decimal
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

# Create your views here.

class APIRoot(APIView):
    #permission_classes = [IsAuthenticated]
    def get(self, request):
        if request.user.is_authenticated:
            # Redirect to the root URL
            """return redirect(reverse('api:api-root'))""" 
            next_url = "/api/" 
            api_root_url = f"{request.build_absolute_uri(reverse('api:api-root'))}?next={next_url}"
            return redirect(api_root_url)
        else:
            return Response({"message": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)      
    
class UserViewset(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


    def create(self, request, *args, **kwargs):
        if not IsAdminUser().has_permission(request, self):
            raise PermissionDenied("Only admins can create users can create users.")
        return super().create(request, *args, **kwargs)


    def update(self, request, *args, **kwargs):
        if not IsAdminUser().has_permission(request, self):
            raise PermissionDenied("Only admins can update users.")
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        if not IsAdminUser().has_permission(request, self):
            raise PermissionDenied("Only admin users can delete users.")
        return super().destroy(request, *args, **kwargs)
    
class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]

class MakeViewSet(viewsets.ModelViewSet):
    queryset = Make.objects.all()
    serializer_class = MakeSerializer
    permission_classes = [IsAuthenticated]

class ModelViewSet(viewsets.ModelViewSet):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    permission_classes = [IsAuthenticated]

class TechnicianViewSet(viewsets.ModelViewSet):
    queryset = Technician.objects.all()
    serializer_class = TechnicianSerializer
    permission_classes = [IsAuthenticated]

class AppointmentsViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

class MaintenanceViewSet(viewsets.ModelViewSet):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer
    permission_classes = [IsAuthenticated]

class MaintenanceTypeViewSets(viewsets.ModelViewSet):
    queryset = MaintenanceType.objects.all()
    serializer_class = MaintenanceTypeSerializer
    permission_classes = [IsAuthenticated]

class RepairViewSet(viewsets.ModelViewSet):
    queryset = Repair.objects.all()
    serializer_class = RepairSerializer
    permission_classes = [IsAuthenticated]

class NotificationsViewSet(viewsets.ModelViewSet):

    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]


# More api urls

class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter] 
    search_fields = ['username', 'email', 'first_name', 'last_name','role__role_name']
    filterset_fields = ['username', 'email', 'is_staff']
    ordering_fields = ['username', 'email', 'first_name', 'last_name','role','is_active','is_staff']    

class UserDetailView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]   

class UserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
       

class UserUpdateView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

class UserDeleteView(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser]    

    def delete(self, request, pk):
        try:
            user = get_object_or_404(CustomUser, pk=pk)

            if not request.user.has_perm('delete_customuser', user):
                raise PermissionDenied('You do not have permissions to delete this user')

            user.delete()

            return Response({'detail': 'User has been deleted successfully'}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ApiLoginView(APIView):
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'here is your token': {token.key}}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#vehicles API's 
class VehicleListView(generics.ListAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter] 
    search_fields = ['owner__first_name','owner__last_name', 'reg_no', 'model__model_name', 'make__make_name','year']
    filterset_fields = ['owner', 'reg_no', 'model__model_name', 'make__make_name','year']
    ordering_fields = ['owner', 'reg_no', 'model__model_name', 'make__make_name','year']

class VehicleCreateView(generics.CreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class VehicleDetailView(generics.RetrieveAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class VehicleUpdateView(generics.UpdateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]    

class VehicleDeleteView(generics.DestroyAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]    

    def delete(self, request, pk):
        try:
            vehicle = get_object_or_404(Vehicle, pk=pk)

            if not request.user.has_perm('delete_vehicle', vehicle):
                raise PermissionDenied('You do not have permissions to delete this vehicle')

            vehicle.delete()

            return Response({'detail': 'vehicle has been deleted successfully'}, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

#make apis

class MakeListView(generics.ListAPIView):
    queryset = Make.objects.all()
    serializer_class = MakeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter] 
    search_fields = ['make_name']
    filterset_fields = ['make_name']
    ordering_fields = ['make_name']

class MakeCreateView(generics.CreateAPIView):
    queryset = Make.objects.all()
    serializer_class = MakeSerializer
    permission_classes = [IsAuthenticated]

class MakeDetailView(generics.RetrieveAPIView):
    queryset = Make.objects.all()
    serializer_class = MakeSerializer
    permission_classes = [IsAuthenticated]

class MakeUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Make.objects.all()
    serializer_class = MakeSerializer
    permission_classes = [IsAuthenticated]

class MakeDeleteView(generics.DestroyAPIView):
    queryset = Make.objects.all()
    serializer_class = MakeSerializer
    permission_classes = [IsAuthenticated]

#Model Api's

class ModelListView(generics.ListAPIView):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    permission_classes = [IsAuthenticated]

class ModelCreateView(generics.CreateAPIView):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    permission_classes = [IsAuthenticated]

class ModelDetailView(generics.RetrieveAPIView):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    permission_classes = [IsAuthenticated]

class ModelUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    permission_classes = [IsAuthenticated]

class ModelDeleteView(generics.DestroyAPIView):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    permission_classes = [IsAuthenticated]

# Technician
class MechanicListView(generics.ListAPIView):
    queryset = Technician.objects.all()
    serializer_class = TechnicianSerializer
    permission_classes = [IsAuthenticated]

class MechanicCreateView(APIView):

    queryset = Technician.objects.all()
    serializer_class = TechnicianSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Check if the user has permission to create a mechanic/technician
            if not request.user.has_perm('garage.add_technician'):  
                raise PermissionDenied("You do not have permission to create technicians.")

            serializer = TechnicianSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({'detail': 'Mechanic created successfully.'}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except PermissionDenied as e:
            return Response({'detail': str(e)}, status=status.HTTP_403_FORBIDDEN)

        except Exception as e:
            return Response({'detail': f'An error occurred: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        
class MechanicDetailView(generics.RetrieveAPIView):
    queryset = Technician.objects.all()
    serializer_class = TechnicianSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class MechanicUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Technician.objects.all()
    serializer_class = TechnicianSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            obj = super().get_object()

            # Check if the user is an admin or the technician is the same as the user
            if not (self.request.user.is_staff or self.request.user.has_perm('garage.change_technician')):
                raise PermissionDenied("You do not have permission to view or edit this mechanic.")

            return obj

        except Technician.DoesNotExist:
            raise PermissionDenied("Mechanic not found.")
        
        except AttributeError: 
            raise PermissionDenied("You do not have permission to view or edit this mechanic.")

        except Exception as e:
            raise PermissionDenied(f"An error occurred: {str(e)}")

class DeleteMechanicView(generics.DestroyAPIView):
    queryset = Technician.objects.all()
    serializer_class = TechnicianSerializer
    permission_classes = [IsAdminUser]   

    def get_object(self):
        try:
            obj = super().get_object()

            # Check if the user is an admin or the technician is the same as the user
            if not (self.request.user.is_staff or self.request.user.has_perm('garage.delete_technician')):
                raise PermissionDenied("You do not have permission to delete this mechanic.")

            return obj

        except Technician.DoesNotExist:
            raise PermissionDenied("Mechanic not found.")
        
        except AttributeError: 
            raise PermissionDenied("You do not have permission to delete this mechanic.")

        except Exception as e:
            raise PermissionDenied(f"An error occurred: {str(e)}")

#maintenances
class MaintenanceListView(generics.ListAPIView):
   
    serializer_class = MaintenanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Maintenance.objects.all()

        elif user.role.role_name == 'customer':
            try:
    
                vehicles = Vehicle.objects.filter(owner=user)    
                if not vehicles.exists():
                    raise PermissionDenied("You do not have permission to view these records.")
                        
                maintenance = Maintenance.objects.filter(vehicle_id__in=vehicles)

                if not maintenance.exists(): 
                    raise PermissionDenied("No maintenance records found for your vehicles.")
                
                return maintenance

            except AttributeError:
                raise PermissionDenied("You do not have permission to view these maintenance.")
        else:
            return Maintenance.objects.none()

class MaintenanceCreateView(generics.CreateAPIView):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer
    permission_classes = [IsAdminUser]

    def post(self, request):
        try:            
            if not request.user.has_perm('garage.add_maintenance'):  
                raise PermissionDenied("You do not have permission to create a maintenance record.")

            serializer = MaintenanceSerializer(data=request.data)

            if serializer.is_valid():
                
                maintenance = serializer.save()

                # Set the maintenance_types relationship.
                maintenance_types_ids = request.POST.getlist('maintenance_types') 
                maintenance.maintenance_types.set(maintenance_types_ids) 

                # Calculate cost and total_cost in the view.
                total_maintenance_cost = sum(mt.maintenance_type_cost for mt in maintenance.maintenance_types.all())
                maintenance.cost = total_maintenance_cost if total_maintenance_cost is not None else Decimal('0.00')
                maintenance.total_cost = (maintenance.cost or Decimal('0.00')) + (maintenance.miscellaneous_cost or Decimal('0.00'))
                maintenance.save() 

                return Response({'detail': 'Maintence created successfully.'}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except PermissionDenied as e:
            return Response({'detail': str(e)}, status=status.HTTP_403_FORBIDDEN)

        except Exception as e:
            return Response({'detail': f'An error occurred: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

class MaintenanceDetailView(generics.RetrieveAPIView):

    serializer_class = MaintenanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

            user = self.request.user        
            if user.is_staff:
                return Maintenance.objects.all()

            elif user.role.role_name == 'customer':
                try:
                    vehicles = Vehicle.objects.filter(owner=user)
                    if not vehicles.exists():
                        raise PermissionDenied("You do not have permission to view these records.")

                    maintenances = Maintenance.objects.filter(vehicle_id__in=vehicles)

                    if not maintenances.exists(): 
                        raise PermissionDenied("No maintenance records found for your vehicles.")
                    return maintenances
                
                except AttributeError:
                    raise PermissionDenied("You do not have permission to view this maintenance.")
            else:
                return Maintenance.objects.none()
                       
class MaintenanceUpdateView(generics.RetrieveUpdateAPIView):
    # queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer
    # permission_classes = [IsAdminUser]

    def get_queryset(self):

        user = self.request.user  
        if user.is_staff:
            return Maintenance.objects.all()
        else:
            raise PermissionDenied("You do not have permission to edit this maintenance.")

    def update(self, request, *args, **kwargs): 
        try:
            instance = self.get_object() 

            if not request.user.has_perm('garage.change_maintenance'):
                raise PermissionDenied("You do not have permission to update a maintenance record.")

            serializer = self.get_serializer(instance, data=request.data) 

            if serializer.is_valid():
                maintenance = serializer.save()

                # Set the maintenance_types relationship.
                maintenance_types_ids = request.POST.getlist('maintenance_types')
                maintenance.maintenance_types.set(maintenance_types_ids)

                # Calculate cost and total_cost in the view.
                total_maintenance_cost = sum(mt.maintenance_type_cost for mt in maintenance.maintenance_types.all())
                maintenance.cost = total_maintenance_cost if total_maintenance_cost is not None else Decimal('0.00')
                maintenance.total_cost = (maintenance.cost or Decimal('0.00')) + (maintenance.miscellaneous_cost or Decimal('0.00'))
                maintenance.save()

                return Response({'detail': 'Maintenance updated successfully.'}, status=status.HTTP_200_OK) 
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except PermissionDenied as e:
            return Response({'detail': str(e)}, status=status.HTTP_403_FORBIDDEN)

        except Exception as e:
            return Response({'detail': f'An error occurred: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

class MaintenanceDeleteView(generics.DestroyAPIView):
    # queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user  
        if user.is_staff:
            return Maintenance.objects.all()
        else:
            raise PermissionDenied("You do not have permission to perform this function.")
    
    def destroy(self, request, *args, **kwargs):
        try:
            
            instance = self.get_object() 

            if not request.user.has_perm('garage.delete_maintenance'):
                raise PermissionDenied("You do not have permission to delete a maintenance record.")
            
            instance.delete()
            return Response({'detail': 'Maintenance deleted successfully.'}, status=status.HTTP_200_OK) 
            
        except PermissionDenied as e:
            return Response({'detail': str(e)}, status=status.HTTP_403_FORBIDDEN)
        
        except Exception as e:
            return Response({'detail': f'An error occurred: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

#repairs 
class RepairsListView(generics.ListAPIView):
    # queryset = Repair.objects.all()
    serializer_class = RepairSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        
        user = self.request.user

        if user.is_staff:
            return Repair.objects.all()
        
        elif user.role.role_name == 'customer':
            try:
                vehicles = Vehicle.objects.filter(owner=user)
                if not vehicles.exists():
                    raise PermissionDenied("You do not have permission to view these records.")

                repairs = Repair.objects.filter(vehicle_id__in=vehicles)
                
                if not repairs.exists(): 
                    raise PermissionDenied("No repair records found for your vehicles.")
                
                return repairs
            
            except AttributeError:
                raise PermissionDenied("You do not have permission to view.")
        
        else:
            return Maintenance.objects.none

class RepairsDetailView(generics.RetrieveAPIView):
    serializer_class = RepairSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

            user = self.request.user        
            if user.is_staff:
                return Repair.objects.all()
            
            elif user.role.role_name == 'customer':
                try:
                    vehicles = Vehicle.objects.filter(owner=user)
                    if not vehicles.exists():
                        raise PermissionDenied("You do not have permission to view these records.")

                    repairs = Repair.objects.filter(vehicle_id__in=vehicles)

                    if not repairs.exists(): 
                        raise PermissionDenied("No repair records found for your vehicles.")
                    
                    return repairs
                
                except AttributeError:
                    raise PermissionDenied("You do not have permission to view.")
            else:
                return Maintenance.objects.none()

class RepairsCreateView(generics.CreateAPIView):
    
    queryset = Repair.objects.all()
    serializer_class = RepairSerializer
    permission_classes = [IsAdminUser] 

    def post(self, request):
        try:
            if not request.user.has_perm('garage.add_repair'):  
                raise PermissionDenied("You do not have permission to create a repair.")

            serializer = RepairSerializer(data=request.data)

            if serializer.is_valid():
                
                serializer.save()                
                return Response({'detail': 'Repair created successfully.'}, status=status.HTTP_200_OK)

            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except PermissionDenied as e:
            return Response({'detail': str(e)}, status=status.HTTP_403_FORBIDDEN)
        
        except Exception as e:
            return Response({'detail': f'An error occurred: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

class RepairsUpdateView(generics.RetrieveUpdateAPIView):
    # queryset = Repair.objects.all()
    serializer_class = RepairSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        user = self.request.user  
        if user.is_staff:
            return Repair.objects.all()
        else:
            raise PermissionDenied("You do not have permission to edit this maintenance.")
    
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object() 

            if not request.user.has_perm('garage.change_repair'):
                raise PermissionDenied("You do not have permission to update a maintenance record.")
            
            serializer = self.get_serializer(instance, data=request.data) 

            if serializer.is_valid():

                serializer.save()
                
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
            return Response({'detail': 'repair updated successfully.'}, status=status.HTTP_200_OK)
        
        except PermissionDenied as e:
            return Response({'detail': str(e)}, status=status.HTTP_403_FORBIDDEN)
        
        except Exception as e:
            return Response({'detail': f'An error occurred: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
    
class RepairDeleteView(generics.DestroyAPIView):
    # queryset = Repair.objects.all()
    serializer_class = RepairSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user  
        if user.is_staff:
            return Repair.objects.all()
        else:
            raise PermissionDenied("You do not have permission to perform this function.")
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if not request.user.has_perm('garage.delete_repair'):
                raise PermissionDenied("You do not have permission to delete this repair record.")

            instance.delete()
            return Response({'detail': 'repair deleted successfully.'}, status=status.HTTP_200_OK)

        except PermissionDenied as e:
            return Response({'detail': str(e)}, status=status.HTTP_403_FORBIDDEN)
        
        except Exception as e:
            return Response({'detail': f'An error occurred: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        
#appointments
class AppointmentListView(generics.ListAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        user = self.request.user
        
        if user.is_staff:
            return Appointment.objects.all()
        
        elif user.role.role_name == 'customer':
            try:
                
                vehicles = Vehicle.objects.filter(owner=user)

                if not vehicles.exists():
                    raise PermissionDenied("You do not have permission to view these records.")

                appointments = Appointment.objects.filter(vehicle_id__in=vehicles)
                
                if not appointments.exists(): 
                    raise PermissionDenied("No appointment records found for your vehicles.")
                
                return appointments
            
            except AttributeError:
                raise PermissionDenied("You do not have permission to view.")
        else:
            return Appointment.objects.none
        
class AppointmentDetailView(generics.RetrieveAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        
        user = self.request.user        
        if user.is_staff:
            return Appointment.objects.all()
        
        elif user.role.role_name == 'customer':
            try:
                vehicles = Vehicle.objects.filter(owner=user)
                if not vehicles.exists():
                    raise PermissionDenied("You do not have permission to view these records.")

                appointments = Appointment.objects.filter(vehicle_id__in=vehicles)

                if not appointments.exists(): 
                    raise PermissionDenied("No appointment records found for your vehicles.")
                
                return appointments
                
            except AttributeError:
                raise PermissionDenied("You do not have permission to view.")
        else:
            return Appointment.objects.none

class AppointmentCreateView(generics.CreateAPIView):

    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            if not request.user.has_perm('garage.add_appointment'):  
                raise PermissionDenied("You do not have permission to create an appointment.")

            serializer = AppointmentSerializer(data=request.data, context={'request': request})

            if serializer.is_valid():
                
                appointment = serializer.save()    
                
                vehicle = appointment.vehicle_id
                owner = vehicle.owner

                email_subject  = 'APPOINTMENT CREATED SUCCESSFULLY'
                email = 'gamisi.ga@gmail.com'
                email_body = render_to_string('api/email.html', {
                    
                    'user': request.user,
                    'owner_full_name': f"{owner.first_name} {owner.last_name}",
                    'appointment_date': appointment.appointment_date,
                    'vehicle_reg_no': vehicle.reg_no,

                })

                send_mail(
                    
                    email_subject, 
                    email_body, 
                    settings.DEFAULT_FROM_EMAIL, [email],
                    html_message=email_body,

                )

                return Response({'detail': 'Appointment created successfully.'}, status=status.HTTP_200_OK)

            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except PermissionDenied as e:
            return Response({'detail': str(e)}, status=status.HTTP_403_FORBIDDEN)
        
        except Exception as e:
            return Response({'detail': f'An error occurred: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

class AppointmentsUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        user = self.request.user  
        if user.is_staff:
            return Appointment.objects.all()
        
        elif user.role and user.role.role_name == 'customer':

            try:
                
                vehicles = Vehicle.objects.filter(owner=user)

                if not vehicles.exists():
                    raise PermissionDenied("You do not have permission to view these records.")

                appointments = Appointment.objects.filter(vehicle_id__in=vehicles)
                
                if not appointments.exists(): 
                    raise PermissionDenied("No appointment records found for your vehicles.")
                
                return appointments

            except AttributeError:
                raise PermissionDenied("You do not have permission perform this fucntion", status=403)
            
        else:
            raise PermissionDenied("You do not have permission to update this appointment.")

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object() 

            if not request.user.has_perm('garage.change_appointment'):
                raise PermissionDenied("You do not have permission to update a this appointment.")
            
            serializer = self.get_serializer(instance, data=request.data) 

            if serializer.is_valid():

                serializer.save()
                
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
            return Response({'detail': 'appointment updated successfully.'}, status=status.HTTP_200_OK)
        
        except PermissionDenied as e:
            return Response({'detail': str(e)}, status=status.HTTP_403_FORBIDDEN)
        
        except Exception as e:
            return Response({'detail': f'An error occurred: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

class AppointmentsDeleteView(generics.DestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        user = self.request.user  
        if user.is_staff:
            return Appointment.objects.all()
        
        elif user.role and user.role.role_name == 'customer':

            try:
                
                vehicles = Vehicle.objects.filter(owner=user)

                if not vehicles.exists():
                    raise PermissionDenied("You do not have permission to view these records.")

                appointments = Appointment.objects.filter(vehicle_id__in=vehicles)
                
                if not appointments.exists(): 
                    raise PermissionDenied("No appointment records found for your vehicles.")
                
                return appointments

            except AttributeError:
                raise PermissionDenied("You do not have permission perform this fucntion", status=403)
            
        else:
            raise PermissionDenied("You do not have permission to update this appointment.")
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()

            #if not request.user.has_perm('garage.delete_repair'):
                # raise PermissionDenied("You do not have permission to delete this appointment.")
            
            instance.delete()

            return Response({'detail': 'appointment deleted successfully.'}, status=status.HTTP_200_OK)

        except PermissionDenied as e:
            return Response({'detail': str(e)}, status=status.HTTP_403_FORBIDDEN)
        
        except Exception as e:
            return Response({'detail': f'An error occurred: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)