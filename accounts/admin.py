from django.contrib import admin
from .models import CustomUser, Role

class CustomUerAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name','email','role', 'is_staff','display_groups','date_joined')

    def display_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()]) 
    display_groups.short_description = 'Groups'

# Register your models here.
admin.site.register(CustomUser,CustomUerAdmin)
admin.site.register(Role)