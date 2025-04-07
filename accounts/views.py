from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets
from .serializers import CustomUserSerializer, UserLoginSerializer
from .models import CustomUser, Role
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.contrib.auth import logout, authenticate
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DetailView, DeleteView
from django.urls import reverse_lazy
from .forms import RegistrationForm, CustomSetPasswordForm, UserEditForm, GroupEditForm, UserProfileForm
from django.contrib.auth import login, logout , authenticate
from django.contrib.auth.views import PasswordResetConfirmView, LoginView
from django.contrib.auth.forms import PasswordResetForm
from django.db.models import F,CharField, Value
from django.db.models.functions import Concat
from django.utils.html import format_html
import os
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Group
from django.http import JsonResponse
from .mixins import RoleRequiredMixin
from accounts.decorators import unauthenticated_user, allowed_users
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from garage.models import Vehicle, Maintenance, Repair, Appointment



"""# Create your views here.
class UserViewset(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer """

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

@unauthenticated_user
def redirect_to_login(request):
    return redirect('login')

def custom_logout(request):
    logout(request)  # This will log the user out
    return redirect('login')  # Redirect to the login page

@unauthenticated_user
def sign_up(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()            
            role = Role.objects.get(role_name = 'customer')            
            user.role = role
            user.save()
            
            email_subject  = 'ACCOUNT CREATED SUCCESSFULLY'
            email = user.email
            email_body = render_to_string('accounts/registration_email.html', {
                
                'user': user,
                
            })

            send_mail(
                
                email_subject, 
                email_body, 
                settings.DEFAULT_FROM_EMAIL, [email],
                html_message=email_body,

            )

            messages.success(request, f'Account created succesfully. An email has been sent to the email you registered with. Your usename is {user.username} . You can go ahead and login to your account')

            return redirect(reverse('sign_up'))
    else:
        form = RegistrationForm()
            
    return render(request,'registration/sign_up.html', {"form": form})

#class based view
class AdminDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'
    login_url =  '/login/'

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            if request.user.role is None:
                raise PermissionDenied
            elif request.user.role.role_name == 'customer': 

                # Redirect to customer dashboard
                return redirect(reverse('customer_dashboard')) 
                              
            else:
                # Render default admin dashboard
                return super().dispatch(request, *args, **kwargs)
        else:
            return self.handle_no_permission()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
                        
        vehicle_count = Vehicle.objects.all().count()        
        maintenance_count = Maintenance.objects.all().count() 
        repair_count = Repair.objects.all().count()        
        appointment_count =  Appointment.objects.all().count()
        open_appointments = Appointment.objects.filter(status='open').count()
        customers = CustomUser.objects.filter(role__role_name='customer').count()

        context['vehicle_count'] = vehicle_count
        context['maintenance_count'] = maintenance_count
        context['repair_count'] = repair_count
        context['appointment_count'] = appointment_count
        context['open_appointments'] = open_appointments
        context['customers'] = customers

        return context

class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'
    login_url = '/login/'
    form_class = UserProfileForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        user = get_object_or_404(CustomUser, id=self.request.user.id) 
        context['form'] = self.form_class(instance=user)
        return context

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(CustomUser, id=self.request.user.id) 
        form = self.form_class(request.POST, instance=user)

        if form.is_valid():
            form.save() 
            
            messages.success(request, 'user updated succesfully.')

        return redirect('user_profile')
             
class CustomerDashboardView(LoginRequiredMixin, RoleRequiredMixin, TemplateView):
    template_name = 'accounts/customer_dashboard.html'
    role_required = 'customer'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        vehicles = Vehicle.objects.filter(owner=user)  

        # Get counts for the logged-in customer
        vehicle_count = Vehicle.objects.filter(owner=user).count()        
        maintenance_count = Maintenance.objects.filter(vehicle_id__in=vehicles).count() 
        repair_count = Repair.objects.filter(vehicle_id__in = vehicles).count()        
        appointment_count =  Appointment.objects.filter(vehicle_id__in = vehicles).count()

        # Add counts to the context
        context['vehicle_count'] = vehicle_count
        context['maintenance_count'] = maintenance_count
        context['repair_count'] = repair_count
        context['appointment_count'] = appointment_count

        return context

def custom_password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            # Send password reset email
            email = form.cleaned_data['email']
            users = CustomUser.objects.filter(email=email)
            for user in users:
                
                # generate reset token and send email
                token = default_token_generator.make_token(user)
                uidb64 = urlsafe_base64_encode(str(user.pk).encode())
                
                # debugging
                """print(f"Generated uidb64: {uidb64}")  
                print(f"Generated token: {token}")"""    

                reset_url = f"http://{get_current_site(request).domain}/reset/{uidb64}/{token}/"

                                
                email_subject = "Password Reset Request"
                email_body = render_to_string('registration/password_email.html', {
                    
                    'reset_url': reset_url,
                    'user': user,
                })
        
                send_mail(
                    
                    email_subject, 
                    email_body, 
                    settings.DEFAULT_FROM_EMAIL, [email],
                    html_message=email_body,
                )
                
            return redirect('password_reset_done')
    else:
        form = PasswordResetForm()

    return render(request, 'registration/password_reset.html', {'form': form})

class SetCustomPasswordView(PasswordResetConfirmView):
    template_name='registration/password_confirm.html' 
    form_class=CustomSetPasswordForm

@method_decorator(allowed_users(), name='dispatch') 
class UserListView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/users-list.html'
    login_url = '/login/'

@method_decorator(allowed_users(), name='dispatch') 
class GroupListView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/groups.html'
    login_url = '/login/' 

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_groups(request):

    groups = Group.objects.annotate().values( "id","name")

    data = []

    for index , group in enumerate(groups):

        edit_url = reverse('edit_group', kwargs={'pk': group['id']})
        
        edit_link = format_html(
            '<a href="{}" class="btn btn-sm btn-info ml-1" title="view group info">'
            '    <i class="fa fa-eye" aria-hidden="true"></i>'
            '</a>',
            edit_url
        )

        data.append({
            
            'rowIndex': index + 1,
            'id': group['id'],
            'name': group['name'],               
            'actions': format_html(

                '<div class="btn-group">'
                    '{}'                    
                    '<button class="btn btn-sm btn-danger ml-1" title="delete group" data-id="{}" id="deleteGroupBtn">'
                        '<i class="fa fa-trash" aria-hidden="true"></i>'
                    '</button>'
                '</div>',

                edit_link, group['id']
            ),
            'checkbox': format_html(

                '<input type="checkbox" name="role_checkbox" data-id="{}"><label></label>',
                group['id']

            ),

        })

    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users(request):
    users = CustomUser.objects.annotate(
        #concat first name and last name
        full_name=Concat(

            F('first_name'), Value(' '), F('last_name'),
            output_field=CharField()
        )

    
    ).values(
        
        # fields that should be selected form the users table
        'id', 'username', 'email', 'full_name', 'role', 'is_active'
    )
    data = []
    for index, user in enumerate(users):

        edit_url = reverse('user_edit', kwargs={'pk': user['id']})
        
        edit_link = format_html(
            '<a href="{}" class="btn btn-sm btn-info ml-1" title="view group info">'
            '    <i class="fa fa-eye" aria-hidden="true"></i>'
            '</a>',
            edit_url
        )

        try:
            role = Role.objects.get(id=user['role'])
            role_name = role.role_name
        except ObjectDoesNotExist:
            role_name = "" 

        data.append({

            'rowIndex': index + 1,
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'full_name': user['full_name'],
            'role_name': role_name,
            'is_status': user['is_active'],
            'actions': format_html(

                '<div class="btn-group">'
                    '{}'                    
                    '<button class="btn btn-sm btn-danger ml-1" title="delete user" data-id="{}" id="deleteUserBtn">'
                        '<i class="fa fa-trash" aria-hidden="true"></i>'
                    '</button>'
                '</div>',

                edit_link, user['id']
            ),
            'checkbox': format_html(

                '<input type="checkbox" name="role_checkbox" data-id="{}"><label></label>',
                user['id']

            ),
        })

    return Response(data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_group(request, pk):

    group = get_object_or_404(Group, pk=pk)

    if not request.user.has_perm('delete_group', group):
        return Response({'detail': 'You do not have permission to delete this group.'}, status=403)
    
    group.delete()
    return Response({'detail': 'Group deleted successfully.'}, status=200)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request, pk):

    user = get_object_or_404(CustomUser, pk=pk)

    if not request.user.has_perm('delete_user', user):
        return Response({'detail': 'You do not have permissions to delete a user'}, status=403)
    
    user.delete()
    return Response({'detail': 'user has been deleted successfully'}, status=200)

@method_decorator(allowed_users(), name='dispatch') 
class UserDetailView(LoginRequiredMixin, TemplateView):
    form_class = UserEditForm
    template_name = 'accounts/view_user.html'  
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk') #get pk from url if available
        if pk:
            user = get_object_or_404(CustomUser, pk=pk)
            context['form'] = self.form_class(instance=user)
        else:
            context['form'] = self.form_class()
        return context
    
    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        if pk:
            user = get_object_or_404(CustomUser, pk=pk)
            form = self.form_class(request.POST, instance=user)
        else:
            form = self.form_class(request.POST)

        if form.is_valid():
            form.save() 
            if pk:       
                return redirect('user_edit', pk=user.pk)     
            else:
                return redirect('users')
        else:
            context = self.get_context_data(pk=pk) #pass pk to context.
            context['form'] = form
            return self.render_to_response(context)

@method_decorator(allowed_users(), name='dispatch') 
class AddGroupView(LoginRequiredMixin, TemplateView):
    form_class = GroupEditForm
    template_name = 'accounts/add_group.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk') #get pk from url if available
        if pk:
            group = get_object_or_404(Group, pk=pk)
            context['form'] = self.form_class(instance=group)
        else:
            context['form'] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        if pk:
            group = get_object_or_404(Group, pk=pk)
            form = self.form_class(request.POST, instance=group)
        else:
            form = self.form_class(request.POST)

        if form.is_valid():
            group = form.save()
            group.permissions.set(form.cleaned_data['permissions'])
            return redirect('group_list')
        else:
            context = self.get_context_data(pk=pk) #pass pk to context.
            context['form'] = form
            return self.render_to_response(context)