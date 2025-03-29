from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    role = models.CharField(max_length=100)
    email = models.EmailField(unique=True, blank=False, null=False)

    def __str__(self):
        return self.username

