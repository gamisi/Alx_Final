from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from .models import Vehicle, Technician, Maintenance
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DetailView, DeleteView
from .forms import AddVehicleForm
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
            model = f"{vehicle.model.model_name}"
            make = f"{vehicle.make.make_name}"

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
    
