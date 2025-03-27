from django.db import models
# from django.contrib.auth.models import User
# Create your models here.
from accounts.models import CustomUser

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
    reg_no = models.CharField(max_length=100)
    user_id = models.ForeignKey(CustomUser, null=True, on_delete=models.RESTRICT, related_name='vehicles')
    model = models.ForeignKey(Model, null=True, on_delete=models.SET_NULL, related_name='vehicles')
    make = models.ForeignKey(Make, null=True, on_delete=models.SET_NULL, related_name='vehicles')
    year = models.IntegerField(null=True)
    
    def __str__(self):
        return self.reg_no

class Technician(models.Model):
    name = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

class MaintenanceType(models.Model):
    maintenance_type_name = models.CharField(max_length=100)
    maintenance_type_cost = models.DecimalField( max_digits=10, decimal_places=2 )
    
    def __str__(self):
        return self.maintenance_type_name

class Maintenance(models.Model):
    vehicle_id = models.ForeignKey(Vehicle, on_delete=models.RESTRICT, related_name='maintenance')
    mechanic = models.ForeignKey(Technician, on_delete=models.RESTRICT, related_name='maintenance')
    maintenance_date = models.DateTimeField(auto_now_add=True)
    maintenance_type = models.ForeignKey(MaintenanceType, on_delete=models.RESTRICT, related_name='maintenance')
    mileage_type = models.IntegerField()

    def __str__(self):
        return self.maintenance_type
    





    