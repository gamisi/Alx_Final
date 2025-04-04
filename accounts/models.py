from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Role (models.Model):
    role_name = models.CharField(max_length=100)
    role_description = models.TextField()

    def __str__(self):
        return self.role_name

class CustomUser(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, related_name='users', null=True, blank=True)
    email = models.EmailField(unique=True, blank=False, null=False)
    
    def __str__(self):
        return self.username

