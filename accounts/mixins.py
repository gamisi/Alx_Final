from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import AccessMixin

class RoleRequiredMixin(AccessMixin):

    role_required = None  
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission(request)
                                
        if self.role_required is None or request.user.role.role_name != self.role_required:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
