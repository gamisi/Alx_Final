from django.contrib import admin
from .models import Model, Make, MaintenanceType, Technician, Maintenance, Vehicle, Appointment, Repair, Notification

# Register your models here.
admin.site.register(Model)
admin.site.register(Make)
admin.site.register(Maintenance)
admin.site.register(MaintenanceType)
admin.site.register(Technician)
admin.site.register(Vehicle)
admin.site.register(Appointment)
admin.site.register(Repair)
admin.site.register(Notification)

