from django.db import models
from django.contrib.auth.models import AbstractUser

from django.conf import settings

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN','Admin'),
        ('MANAGER','Manager'),
        ('EMPLOYEE','Employee'),
    )
    role = models.CharField(max_length=10,default='EMPLOYEE', choices=ROLE_CHOICES)

    def __str__(self):
        return self.username
    
class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='created_projects')
    employees = models.ManyToManyField(User,related_name='assigned_projects',blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
