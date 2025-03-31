from django.contrib import admin
from .models import CustomUser, Role

class CustomUerAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name','email','role', 'is_staff','date_joined')

# Register your models here.
admin.site.register(CustomUser,CustomUerAdmin)
admin.site.register(Role)