from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROL_CHOICES = [
        ('cliente', 'Cliente'),
        ('gerente', 'Gerente'),
    ]
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='cliente')
