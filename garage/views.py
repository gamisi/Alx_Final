from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from .models import Vehicle, Technician, Maintenance, Make, Model, MaintenanceType, Repair, Appointment
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DetailView, DeleteView
from .forms import AddVehicleForm, MakeForm, ModelForm, TechnicianForm, RepairForm, MaintenanceForm, NotificationForm, AppointmentForm
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.

#class based view
class VehicleListView(LoginRequiredMixin, TemplateView):
    template_name = 'garage/list_vehicles.html'
    login_url =  '/login/'

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_vehicles(request):
    try:
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
            context['form'] = self.form_class(instance=vehicle)
        else:
            context['form'] = self.form_class()
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
    
class MakeView(LoginRequiredMixin, TemplateView):
    template_name = 'garage/makes.html'
    login_url = '/login'

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

class TechnicianView(LoginRequiredMixin, TemplateView):
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