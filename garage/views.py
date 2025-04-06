from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from .models import Vehicle, Technician, Maintenance, Make, Model, MaintenanceType, Repair, Appointment
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DetailView, DeleteView
from .forms import AddVehicleForm, MakeForm, ModelForm, TechnicianForm, RepairForm, MaintenanceForm, NotificationForm, AppointmentForm, MaintenanceTypeForm
from django.shortcuts import render, get_object_or_404, redirect
from decimal import Decimal
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from accounts.decorators import allowed_users
from django.utils.decorators import method_decorator
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

# Create your views here.

#class based view
class VehicleListView(LoginRequiredMixin, TemplateView):
    template_name = 'garage/list_vehicles.html'
    login_url =  '/login/'

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_vehicles(request):
    try:

        id = request.user.id
        if request.user.role.role_name == 'customer':
            vehicles = Vehicle.objects.filter(owner_id=id) 
        else:
            vehicles = Vehicle.objects.all()

        data = []

        for index, vehicle in enumerate(vehicles):
            edit_url = reverse('edit_vehicle', kwargs={'pk': vehicle.id}) 

            edit_link = format_html(
                '<a href="{}" class="btn btn-sm btn-info ml-1" title="view vehicle info">'
                '    <i class="fa fa-eye" aria-hidden="true"></i>'
                '</a>',
                edit_url
            )

            owner_name = f"{vehicle.owner.first_name} {vehicle.owner.last_name}" if vehicle.owner else None
            model = f"{vehicle.model.model_name}" if vehicle.model else None
            make = f"{vehicle.make.make_name}" if vehicle.make else None

            data.append({
                'rowIndex': index + 1,
                'id': vehicle.id,
                'reg_no': vehicle.reg_no, 
                'owner': owner_name,
                'model': model,
                'make': make,
                'year': vehicle.year,                
                'actions': format_html(
                    '<div class="btn-group">'
                    '    {}'
                    '    <button class="btn btn-sm btn-danger ml-1" title="delete vehicle" data-id="{}" id="deleteVehicleBtn">'
                    '        <i class="fa fa-trash" aria-hidden="true"></i>'
                    '    </button>'
                    '</div>',
                    edit_link, vehicle.id
                ),
                'checkbox': format_html(
                    '<input type="checkbox" name="role_checkbox" data-id="{}"><label></label>',
                    vehicle.id
                ),
            })

        return Response(data)

    except Exception as e:
        return Response({'error': str(e)}, status=500)

class AddVehicleView(LoginRequiredMixin, TemplateView):
    form_class = AddVehicleForm
    template_name = 'garage/add_vehicle.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk') #get pk from url if available
        if pk:
            vehicle = get_object_or_404(Vehicle, pk=pk)

            if self.request.user.role.role_name == 'customer':
                if vehicle.owner != self.request.user:
                    raise PermissionDenied
                
            context['form'] = self.form_class(instance=vehicle, user=self.request.user)

        else:
            context['form'] = self.form_class(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        if pk:
            vehicle = get_object_or_404(Vehicle, pk=pk)
            form = self.form_class(request.POST, instance=vehicle)
        else:
            form = self.form_class(request.POST)

        if form.is_valid():
            vehicle = form.save()
            if pk:       
                return redirect('edit_vehicle', pk=vehicle.pk)     
            else:
                return redirect('all_vehicles')
        else:
            context = self.get_context_data(pk=pk) #pass pk to context.
            context['form'] = form
            return self.render_to_response(context)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_vehicle(request, pk):
    try:

        vehicle = get_object_or_404(Vehicle, pk=pk)
        if not request.user.has_perm('delete_vehicle', vehicle):
            return Response({'detail': 'You do not have permissions to delete a vehicle'}, status=403)
        
        vehicle.delete()

        return Response({'detail': 'vehicle has been deleted successfully'}, status=200)

    except Exception as e:
        return Response({'error': str(e)}, status=403)
    
@method_decorator(allowed_users(), name='dispatch')
class MakeView(LoginRequiredMixin, TemplateView):
    template_name = 'garage/makes.html'
    login_url = '/login'

@method_decorator(allowed_users(), name='dispatch')
class ModelView(LoginRequiredMixin, TemplateView):
    template_name = 'garage/models.html'
    login_url = '/login'

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_makes(request):

    try:
        makes = Make.objects.all()
        data = []

        for index, make in enumerate(makes):

            edit_url =  reverse('edit_make', kwargs={'pk': make.id})
            edit_link = format_html(
                '<a href="{}" class="btn btn-sm btn-info ml-1" title="view make">'
                '    <i class="fa fa-eye" aria-hidden="true"></i>'
                '</a>',
                edit_url
            )

            data.append({
                'rowIndex': index + 1,
                'id': make.id,
                'make_name': make.make_name, 
                'make_desc': make.make_desc,               
                'actions': format_html(
                    '<div class="btn-group">'
                    '    {}'
                    '    <button class="btn btn-sm btn-danger ml-1" title="delete vehicle" data-id="{}" id="deleteMakeBtn">'
                    '        <i class="fa fa-trash" aria-hidden="true"></i>'
                    '    </button>'
                    '</div>',
                    edit_link, make.id
                ),
                'checkbox': format_html(
                    '<input type="checkbox" name="role_checkbox" data-id="{}"><label></label>',
                    make.id
                ),
            })

        return Response(data)

    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_models(request):

    try:
        models = Model.objects.all()
        data = []

        for index, model in enumerate(models):

            edit_url =  reverse('edit_model', kwargs={'pk': model.id})
            edit_link = format_html(
                '<a href="{}" class="btn btn-sm btn-info ml-1" title="view model">'
                '    <i class="fa fa-eye" aria-hidden="true"></i>'
                '</a>',
                edit_url
            )

            data.append({
                'rowIndex': index + 1,
                'id': model.id,
                'model_name': model.model_name, 
                'model_desc': model.model_desc,               
                'actions': format_html(
                    '<div class="btn-group">'
                    '    {}'
                    '    <button class="btn btn-sm btn-danger ml-1" title="delete vehicle" data-id="{}" id="deleteBtn">'
                    '        <i class="fa fa-trash" aria-hidden="true"></i>'
                    '    </button>'
                    '</div>',
                    edit_link, model.id
                ),
                'checkbox': format_html(
                    '<input type="checkbox" name="role_checkbox" data-id="{}"><label></label>',
                    model.id
                ),
            })

        return Response(data)

    except Exception as e:
        return Response({'error': str(e)}, status=500)

@method_decorator(allowed_users(), name='dispatch')
class AddModelView(LoginRequiredMixin, TemplateView):
    form_class = ModelForm
    template_name = 'garage/view_models.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk') #get pk from url if available
        if pk:
            model = get_object_or_404(Model, pk=pk)
            context['form'] = self.form_class(instance=model)
        else:
            context['form'] = self.form_class()
        return context
    
    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        if pk:
            model = get_object_or_404(Model, pk=pk)
            form = self.form_class(request.POST, instance=model)
        else:
            form = self.form_class(request.POST)

        if form.is_valid():
            model = form.save()
            if pk:       
                return redirect('edit_model', pk=model.pk)     
            else:
                return redirect('all_models')
        else:
            context = self.get_context_data(pk=pk) 
            context['form'] = form
            return self.render_to_response(context)

@method_decorator(allowed_users(), name='dispatch')
class AddMakeView(LoginRequiredMixin, TemplateView):
    form_class = MakeForm
    template_name = 'garage/view_makes.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk') #get pk from url if available
        if pk:
            make = get_object_or_404(Make, pk=pk)
            context['form'] = self.form_class(instance=make)
        else:
            context['form'] = self.form_class()
        return context
    
    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        if pk:
            make = get_object_or_404(Make, pk=pk)
            form = self.form_class(request.POST, instance=make)
        else:
            form = self.form_class(request.POST)

        if form.is_valid():
            make = form.save()
            if pk:       
                return redirect('edit_make', pk=make.pk)     
            else:
                return redirect('all_makes')
        else:
            context = self.get_context_data(pk=pk) 
            context['form'] = form
            return self.render_to_response(context)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_make(request, pk):
    try:
        make = get_object_or_404(Make, pk=pk)
        if not request.user.has_perm('delete_make', make):
            return Response({'detail': 'You do not have permissions to delete a make'}, status=403)
        
        make.delete()
        return Response({'detail': 'make has been deleted successfully'}, status=200)

    except Exception as e:
        return Response({'error': str(e)}, status=403)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_model(request, pk):
    try:
        model = get_object_or_404(Model, pk=pk)
        if not request.user.has_perm('delete_model', model):
            return Response({'detail': 'You do not have permissions to delete a model'}, status=403)
        
        model.delete()
        return Response({'detail': 'model has been deleted successfully'}, status=200)

    except Exception as e:
        return Response({'error': str(e)}, status=403)

@method_decorator(allowed_users(), name='dispatch')
class MechanicView(LoginRequiredMixin, TemplateView):
    template_name = 'garage/technicians.html'
    login_url = '/login/'

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_technicians(request):

    try:

        mechanics = Technician.objects.all()
        data = []

        for index, mechanic in enumerate(mechanics):
 
                edit_url =  reverse('edit_mechanic', kwargs={'pk': mechanic.id})
                edit_link = format_html(
                    '<a href="{}" class="btn btn-sm btn-info ml-1" title="view make">'
                    '    <i class="fa fa-eye" aria-hidden="true"></i>'
                    '</a>',
                    edit_url
                )

                data.append({
                    'rowIndex': index + 1,
                    'id': mechanic.id,
                    'name': mechanic.name, 
                    'phone_no': mechanic.phone_no,
                    'specialty': mechanic.specialty,
                    'actions': format_html(
                        '<div class="btn-group">'
                        '    {}'
                        '    <button class="btn btn-sm btn-danger ml-1" title="delete vehicle" data-id="{}" id="deleteBtn">'
                        '        <i class="fa fa-trash" aria-hidden="true"></i>'
                        '    </button>'
                        '</div>',
                        edit_link, mechanic.id
                    ),
                    'checkbox': format_html(
                        '<input type="checkbox" name="role_checkbox" data-id="{}"><label></label>',
                        mechanic.id
                    ),
                })

        return Response(data)

    except Exception as e:
        return Response({'error': str(e)}, status=500)

@method_decorator(allowed_users(), name='dispatch')
class AddMechanicView(LoginRequiredMixin, TemplateView):
    form_class = TechnicianForm
    template_name = 'garage/view_technician.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk') 
        if pk:
            mechanic = get_object_or_404(Technician, pk=pk)
            context['form'] = self.form_class(instance=mechanic)
        else:
            context['form'] = self.form_class()
        return context
    
    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        if pk:
            mechanic = get_object_or_404(Technician, pk=pk)
            form = self.form_class(request.POST, instance=mechanic)
        else:
            form = self.form_class(request.POST)

        if form.is_valid():
            mechanic = form.save()
            if pk:       
                return redirect('edit_mechanic', pk=mechanic.pk)     
            else:
                return redirect('all_mechanics')
        else:
            context = self.get_context_data(pk=pk) 
            context['form'] = form
            return self.render_to_response(context)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_mechanic(request, pk):
    try:
        mechanic = get_object_or_404(Technician, pk=pk)
        if not request.user.has_perm('delete_mechanic', mechanic):
            return Response({'detail': 'You do not have permissions to delete a mechanic'}, status=403)
        
        mechanic.delete()
        return Response({'detail': 'mechanic has been deleted successfully'}, status=200)

    except Exception as e:
        return Response({'error': str(e)}, status=403)

@method_decorator(allowed_users(), name='dispatch')
class MaintenanceTypeView(LoginRequiredMixin, TemplateView):
    template_name = 'garage/maintenancetype.html'
    login_url = '/login/'

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_maintenance_types(request):

    try:

        maintenancetypes = MaintenanceType.objects.all()
        data = []

        for index, maintenancetype in enumerate(maintenancetypes):
            
                
                edit_url = reverse('edit_maintenance_type', kwargs={'pk': maintenancetype.id})
                edit_link = format_html(
                    '<a href="{}" class="btn btn-sm btn-info ml-1" title="view maintenance type">'
                    '    <i class="fa fa-eye" aria-hidden="true"></i>'
                    '</a>',
                    edit_url
                )

                data.append({
                    'rowIndex': index + 1,
                    'id': maintenancetype.id,
                    'maintenance_type_name': maintenancetype.maintenance_type_name, 
                    'maintenance_type_cost': maintenancetype.maintenance_type_cost,
                    'maintenance_type_desc': maintenancetype.maintenance_type_desc,
                    'actions': format_html(
                        '<div class="btn-group">'
                        '    {}'
                        '    <button class="btn btn-sm btn-danger ml-1" title="delete vehicle" data-id="{}" id="deleteBtn">'
                        '        <i class="fa fa-trash" aria-hidden="true"></i>'
                        '    </button>'
                        '</div>',
                        edit_link, maintenancetype.id
                    ),
                    'checkbox': format_html(
                        '<input type="checkbox" name="role_checkbox" data-id="{}"><label></label>',
                        maintenancetype.id
                    ),
                })

        return Response(data)
        
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@method_decorator(allowed_users(), name='dispatch')
class AddMaintenancetypeView(LoginRequiredMixin, TemplateView):
    form_class = MaintenanceTypeForm
    template_name = 'garage/view_maintenancetype.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk') 
        if pk:
            maintenancetype = get_object_or_404(MaintenanceType, pk=pk)
            context['form'] = self.form_class(instance=maintenancetype)
        else:
            context['form'] = self.form_class()
        return context
    
    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        if pk:
            maintenancetype = get_object_or_404(MaintenanceType, pk=pk)
            form = self.form_class(request.POST, instance=maintenancetype)
        else:
            form = self.form_class(request.POST)

        if form.is_valid():
            maintenancetype = form.save()
            if pk:       
                return redirect('edit_maintenance_type', pk=maintenancetype.pk)     
            else:
                return redirect('maintenance_types')
        else:
            context = self.get_context_data(pk=pk) 
            context['form'] = form
            return self.render_to_response(context)

@api_view(['DELETE']) 
@permission_classes([IsAuthenticated])  
def delete_maintenance_type(request, pk):

    try:
        maintenance_type = get_object_or_404(MaintenanceType, pk=pk)
        if not request.user.has_perm('delete_maintenance_type', maintenance_type):
            return Response({'detail': 'You do not have permissions to delete a mechanic'}, status=403)
        
        maintenance_type.delete()
        return Response({'detail': 'maintenance_type has been deleted successfully'}, status=200)

    except Exception as e:
        return Response({'error': str(e)}, status=403)


class MaintenanceView(LoginRequiredMixin, TemplateView):
    template_name = 'garage/maintenance.html'
    login_url = '/login/'
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_maintenances(request):

    try:

        user = request.user

        if user.role.role_name == 'customer':
            # Get the user's vehicles.
            vehicles = Vehicle.objects.filter(owner=user)  
            maintenances = Maintenance.objects.filter(vehicle_id__in=vehicles) 
        else:
            maintenances = Maintenance.objects.all()

        data = []

        for index, maintenance in enumerate(maintenances):
            
                maintenance_types_data = []
                for mt in maintenance.maintenance_types.all():
                    maintenance_types_data.append({
                        'id': mt.id,
                        'maintenance_types': mt.maintenance_type_name  + ' - ' + str(mt.maintenance_type_cost),
                        # 'maintenance_type_cost': str(mt.maintenance_type_cost), 
                        # 'maintenance_type_desc': mt.maintenance_type_desc,
                    })
                
                edit_url = reverse('edit_maintenance', kwargs={'pk': maintenance.id})
                edit_link = format_html(
                    '<a href="{}" class="btn btn-sm btn-info ml-1" title="view maintenance type">'
                    '    <i class="fa fa-eye" aria-hidden="true"></i>'
                    '</a>',
                    edit_url
                )

                actions = ''

                if request.user.is_staff:                    
                    actions = format_html(
                        
                        '<div class="btn-group">'
                        '    {}'
                        '    <button class="btn btn-sm btn-danger ml-1" title="delete vehicle" data-id="{}" id="deleteBtn">'
                        '        <i class="fa fa-trash" aria-hidden="true"></i>'
                        '    </button>'
                        '</div>',
                        edit_link, maintenance.id
                    )

                data.append({

                    'rowIndex': index + 1,
                    'id': maintenance.id,                    
                    'vehicle': maintenance.vehicle_id.reg_no, 
                    'mechanic': maintenance.mechanic.name,
                    'maintenance_date': maintenance.maintenance_date,
                    'maintenance_types': maintenance_types_data,
                    'mileage': maintenance.mileage,
                    'cost': maintenance.cost,
                    'miscellaneous_cost': maintenance.miscellaneous_cost,
                    'total_cost': maintenance.total_cost,
                    'actions': actions,
                    'checkbox': format_html(
                        '<input type="checkbox" name="role_checkbox" data-id="{}"><label></label>',
                        maintenance.id
                    ),
                })

        return Response(data)
        
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@method_decorator(allowed_users(), name='dispatch')
class AddMaintenanceView(LoginRequiredMixin, TemplateView):
    form_class  = MaintenanceForm
    template_name = 'garage/view_maintenance.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk') 
        if pk:
            maintenance = get_object_or_404(Maintenance, pk=pk)
            context['form'] = self.form_class(instance=maintenance)
        else:
            context['form'] = self.form_class()
        return context
    
    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        if pk:
            maintenance = get_object_or_404(Maintenance, pk=pk)
            form = self.form_class(request.POST, instance=maintenance)
        else:
            form = self.form_class(request.POST)

        if form.is_valid():
            
            maintenance = form.save()

            # Set the maintenance_types relationship.
            maintenance_types_ids = request.POST.getlist('maintenance_types') 
            maintenance.maintenance_types.set(maintenance_types_ids) 

            # Calculate cost and total_cost in the view.
            total_maintenance_cost = sum(mt.maintenance_type_cost for mt in maintenance.maintenance_types.all())
            maintenance.cost = total_maintenance_cost if total_maintenance_cost is not None else Decimal('0.00')
            maintenance.total_cost = (maintenance.cost or Decimal('0.00')) + (maintenance.miscellaneous_cost or Decimal('0.00'))
            maintenance.save() 

            if pk:       
                return redirect('edit_maintenance', pk=maintenance.pk)     
            else:
                return redirect('all_maintenances')
        else:
            context = self.get_context_data(pk=pk) 
            context['form'] = form
            return self.render_to_response(context)


class RepairsView(LoginRequiredMixin, TemplateView):
    template_name = 'garage/all_repairs.html'
    login_url = '/login/' 

@method_decorator(allowed_users(), name='dispatch')
class AddRepairsView(LoginRequiredMixin, TemplateView):
    form_class = RepairForm
    template_name = 'garage/view_repairs.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        pk = self.kwargs.get('pk')
        if pk:
            repair = get_object_or_404(Repair, pk=pk)
            context['form'] = self.form_class(instance=repair)
        else:
            context['form'] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        if pk:
            repair = get_object_or_404(Repair, pk=pk)
            form = self.form_class(request.POST, instance=repair)
        else:
            form = self.form_class(request.POST)

        if form.is_valid():
            
            repair = form.save()
            if pk:       
                return redirect('edit_repair', pk=repair.pk)     
            else:
                return redirect('all_repairs')
                    
        else:
            context = self.get_context_data(pk=pk) 
            context['form'] = form
            return self.render_to_response(context)    
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_repairs(request):

    user = request.user

    if user.role.role_name == 'customer':
        vehicles = Vehicle.objects.filter(owner=user)  # Get the user's vehicles.
        repairs = Repair.objects.filter(vehicle_id__in=vehicles) #filter repairs
    else:
        repairs = Repair.objects.all()
    
    data = []

    try:
        for index, repair in enumerate(repairs):

            edit_url = reverse('edit_repair', kwargs={'pk': repair.id})
            edit_link = format_html(
                '<a href="{}" class="btn btn-sm btn-info ml-1" title="view maintenance type">'
                '    <i class="fa fa-eye" aria-hidden="true"></i>'
                '</a>',
                edit_url
            )

            actions = ''

            if request.user.is_staff:
                actions = format_html(

                    '<div class="btn-group">'
                        '{}'
                        '<button class="btn btn-sm btn-danger ml-1" title="delete vehicle" data-id="{}" id="deleteBtn">'
                            '<i class="fa fa-trash" aria-hidden="true"></i>'
                        '</button>'
                    '</div>',
                    edit_link, repair.id

                )

            data.append({

                'rowIndex': index + 1,
                'id': repair.id,  
                'vehicle': repair.vehicle_id.reg_no,     
                'mechanic': repair.mechanic.name,
                'repair_date': repair.repair_date,
                'repair_cost': repair.repair_cost,
                'description': repair.description,             
                'actions': actions,
                'checkbox': format_html(
                    '<input type="checkbox" name="role_checkbox" data-id="{}"><label></label>',
                    repair.id
                ),
            })
        
        return Response(data)
        
    
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_repair(request, pk):
    try:
        repair = get_object_or_404(Repair, pk=pk)
        if not request.user.has_perm('delete_repair', repair):
            return Response({'detail': 'You do not have permissions to this repair'}, status=403)
        
        repair.delete()

        return Response({'detail': 'repair record has been deleted successfully'}, status=200)

    except Exception as e:
        return Response({'error': str(e)}, status=403)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_maintenance(request, pk):
    try:
        maintenance = get_object_or_404(Maintenance, pk=pk)
        if not request.user.has_perm('delete_maintenance', maintenance):
            return Response({'detail': 'You do not have permissions to delete a maintenance'}, status=403)
        
        maintenance.delete()

        return Response({'detail': 'maintenance has been deleted successfully'}, status=200)

    except Exception as e:
        return Response({'error': str(e)}, status=403)


class AppointmentView(LoginRequiredMixin, TemplateView):
    template_name = 'garage/appointments.html'
    login_url = '/login/'

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_appointments(request):
    
    try:

        user = request.user

        if user.role.role_name == 'customer':

            vehicles = Vehicle.objects.filter(owner=user)
            appointments= Appointment.objects.filter(vehicle_id__in=vehicles) 

        else:
            appointments = Appointment.objects.all()    

        data = []

        for index, appointment in enumerate(appointments):

                edit_url = reverse('edit_appointment', kwargs={'pk': appointment.id})
                edit_link = format_html(
                    '<a href="{}" class="btn btn-sm btn-info ml-1" title="view maintenance type">'
                    '    <i class="fa fa-eye" aria-hidden="true"></i>'
                    '</a>',
                    edit_url
                )

                # Format the datetime to be readable.
                if appointment.appointment_date:
                    readable_date = appointment.appointment_date.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    readable_date = None

                data.append({

                        'rowIndex': index + 1,
                        'id': appointment.id,  
                        'vehicle': appointment.vehicle_id.reg_no,     
                        'owner': appointment.vehicle_id.owner.username if appointment.vehicle_id.owner else None,
                        'appointment_date': readable_date,
                        'description': appointment.description, 
                        'status': appointment.status,            
                        'actions': format_html(
                            '<div class="btn-group">'
                            '    {}'
                            '    <button class="btn btn-sm btn-danger ml-1" title="delete vehicle" data-id="{}" id="deleteBtn">'
                            '        <i class="fa fa-trash" aria-hidden="true"></i>'
                            '    </button>'
                            '</div>',
                            edit_link, appointment.id
                        ),
                        'checkbox': format_html(
                            '<input type="checkbox" name="role_checkbox" data-id="{}"><label></label>',
                            appointment.id
                        ),

                })

        return Response(data)
    
    except Exception as e:
        return Response({"Error": str(e)}, status=500 )
    

class AddAppoitnmentView(LoginRequiredMixin, TemplateView):
    form_class = AppointmentForm
    template_name = 'garage/view_appointment.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        if pk:
            appointment = get_object_or_404(Appointment, pk=pk)
            vehicle = get_object_or_404(Vehicle, reg_no=appointment.vehicle_id)           
            
            # print(appointment.vehicle_id)
            
            if self.request.user.role.role_name == 'customer':
                if vehicle.owner != self.request.user:
                    #return Http404("Appointment not found or not yours.")
                    raise PermissionDenied
                                        
            context['form'] = self.form_class(instance=appointment, user=self.request.user)

        else:
            context['form'] = self.form_class(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        if pk:
            appointment = get_object_or_404(Appointment, pk=pk)
            form = self.form_class(request.POST, instance=appointment, user=request.user)
        else:
            form = self.form_class(request.POST, user=request.user)

        if form.is_valid():
            
            appointment = form.save()

            vehicle = appointment.vehicle_id
            owner = vehicle.owner

            email_subject  = 'APPOINTMENT CREATED SUCCESSFULLY'
            email = 'gamisi.ga@gmail.com'
            email_body = render_to_string('garage/email.html', {
                
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

            if pk:       
                return redirect('edit_appointment', pk=appointment.pk)     
            else:
                return redirect('all_appointments')
                    
        else:
            context = self.get_context_data(pk=pk) 
            context['form'] = form
            return self.render_to_response(context)    

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_appointment(request, pk):
    try:
        appointment = get_object_or_404(Appointment, pk=pk)

        print(f"User Permissions: {request.user.get_all_permissions()}")

        if not request.user.has_perm('garage.delete_appointment', appointment):
            return Response({'detail': 'You do not have permissions to delete an appointment'}, status=403)
        
        appointment.delete()

        return Response({'detail': 'appointment has been deleted successfully'}, status=200)

    except Exception as e:
        return Response({'error': str(e)}, status=403)