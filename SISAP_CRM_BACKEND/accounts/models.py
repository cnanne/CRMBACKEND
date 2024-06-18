# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=255)
    key = models.CharField(max_length=255, unique=True)
    permissions = models.ManyToManyField('Permission')

    def __str__(self):
        return self.name

class Permission(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    roles = models.ManyToManyField(Role, related_name='users')
    photo = models.ImageField(upload_to='user_photos/', null=True, blank=True)

# Ensure AUTH_USER_MODEL in settings.py points to this model
