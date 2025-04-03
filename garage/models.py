from django.db import models
# from django.contrib.auth.models import User
from accounts.models import CustomUser
from decimal import Decimal

# Create your models here.
class Model(models.Model):
    model_name = models.CharField(max_length=100)
    model_desc = models.TextField()

    def __str__(self):
        return self.model_name

class Make(models.Model):
    make_name = models.CharField(max_length=100)
    make_desc = models.TextField()

    def __str__(self):
        return self.make_name

class Vehicle(models.Model):
    reg_no = models.CharField(max_length=100, unique=True)
    owner = models.ForeignKey(CustomUser, null=True, on_delete=models.RESTRICT, related_name='vehicles')
    model = models.ForeignKey(Model, null=True, on_delete=models.SET_NULL, blank=True, related_name='vehicles')
    make = models.ForeignKey(Make, null=True, on_delete=models.SET_NULL, blank=True, related_name='vehicles')
    year = models.IntegerField(null=True)
    
    def __str__(self):
        return self.reg_no

class Technician(models.Model):
    name = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=100, null=True)
    specialty = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

class MaintenanceType(models.Model):
    maintenance_type_name = models.CharField(max_length=100)
    maintenance_type_cost = models.DecimalField( max_digits=10, decimal_places=2, null=True, default=0 )
    maintenance_type_desc = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.maintenance_type_name

class Maintenance(models.Model):
    vehicle_id = models.ForeignKey(Vehicle, on_delete=models.RESTRICT, related_name='maintenance')
    mechanic = models.ForeignKey(Technician, on_delete=models.RESTRICT, related_name='maintenance')
    maintenance_types = models.ManyToManyField(MaintenanceType, blank=True ,related_name='maintenances')  # ManyToManyField for multiple types
    mileage = models.IntegerField()
    maintenance_date = models.DateField(null=True ,blank=True)
    miscellaneous_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)

    #moved method to the view
    """def save(self, *args, **kwargs):
        # Calculate cost based on selected maintenance types
        total_maintenance_cost = sum(mt.maintenance_type_cost for mt in self.maintenance_types.all())
        self.cost = total_maintenance_cost if total_maintenance_cost is not None else Decimal('0.00')

        # Calculate total cost
        self.total_cost = (self.cost or Decimal('0.00')) + (self.miscellaneous_cost or Decimal('0.00'))

        super().save(*args, **kwargs)"""

    def __str__(self):
        return f"Maintenance for {self.vehicle_id} on {self.maintenance_date}"

class Repair(models.Model):
    vehicle_id = models.ForeignKey(Vehicle, on_delete=models.RESTRICT, related_name='repairs')
    mechanic = models.ForeignKey(Technician, on_delete=models.RESTRICT, related_name='repairs')    
    repair_date = models.DateField(null=True)
    repair_cost = models.DecimalField( max_digits=10, decimal_places=2, blank=True, null=True )
    description = models.TextField(blank=True)

class Appointment(models.Model):
    # user_id = models.ForeignKey(CustomUser, null=True, on_delete=models.RESTRICT, related_name='appointments')    
    STATUS_CHOICES = (

        ('open', 'Open'),
        ('closed', 'Closed'),
    )
    vehicle_id = models.ForeignKey(Vehicle, on_delete=models.RESTRICT, related_name='appointments')    
    appointment_date = models.DateTimeField(null=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES ,default='open')

class Notification(models.Model):
    user_id = models.ForeignKey(CustomUser, null=True, on_delete=models.RESTRICT, related_name='notifications')
    message = models.CharField(max_length=100)
    notification_date = models.DateTimeField()
    notification_type = models.CharField(max_length=100)
    Is_read = models.BooleanField(default=0)


