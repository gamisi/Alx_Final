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
from .forms import RegistrationForm, CustomSetPasswordForm, UserEditForm, GroupEditForm
from django.contrib.auth import login, logout , authenticate
from django.contrib.auth.views import PasswordResetConfirmView
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

"""# Create your views here.
class UserViewset(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class UserLoginView(APIView):
    
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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)"""

def custom_logout(request):
    logout(request)  # This will log the user out
    return redirect(reverse('login'))  # Redirect to the login page

def sign_up(request):

    """page_title = os.path.splitext(os.path.basename('registration/sign_up.html'))[0].capitalize()
    context = {

        'page_title': page_title,
    }"""

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            #login(request, user)
            return redirect('/sign-up')
    else:
        form = RegistrationForm()
            
    return render(request,'registration/sign_up.html', {"form": form})

#class based view
class AdminDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'
    login_url =  '/login/'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.role.role_name == 'customer':
                # Redirect to customer dashboard
                return redirect(reverse('customer_dashboard'))
            else:
                # Render default admin dashboard
                return super().dispatch(request, *args, **kwargs)
        else:
            return self.handle_no_permission(request)

class CustomerDashboardView(LoginRequiredMixin, RoleRequiredMixin, TemplateView):
    template_name = 'accounts/customer_dashboard.html'
    role_required = 'customer'
    login_url = '/login/'

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

class UserListView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/users-list.html'
    login_url = '/login/'

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
        'id', 'username', 'email', 'full_name', 'role'
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