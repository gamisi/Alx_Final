from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):

        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return view_func(request, *args, **kwargs)
        
    return wrapper_func


def allowed_users(allowed_roles=None):
    if allowed_roles is None:
        allowed_roles = []

    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):    
            if request.user.is_anonymous:
                return redirect('/login/?next=' + request.path) 
            if request.user.is_staff: #check for staff status.
                print("User is staff.")
                return view_func(request, *args, **kwargs)
            else:
                print("User is not staff.")
                return HttpResponseForbidden("You do not have permission to access this page.")
        return wrapper_func
    return decorator        
