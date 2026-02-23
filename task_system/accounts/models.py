from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Custom User model extending Django's built-in AbstractUser
# This allows us to add extra fields (like role) to the default user
class User(AbstractUser):

    # Role choices for role-based access control (RBAC)
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('MANAGER', 'Manager'),
        ('EMPLOYEE', 'Employee'),
    )
    # Each user must have a role
    # Default role is EMPLOYEE
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='EMPLOYEE'
    )
    # String representation used in admin and shell
    def __str__(self):
        return self.username

# Project model represents a work project created by a Manager/Admin
class Project(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_projects'
    )
    # Employees assigned to work on this project
    # ManyToMany = Many employees can work on many projects
    employees = models.ManyToManyField(
        User,
        related_name='assigned_projects',
        blank=True
    )
    # Automatically stores project creation timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    # String representation for admin display
    def __str__(self):
        return self.name