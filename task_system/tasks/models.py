from django.db import models
from django.conf import settings
from accounts.models import Project

class Task(models.Model):
    STATUS_CHOICE=(
        ('PENDING','Pending'),
        ('SUBMITTED','Submitted'),
        ('APPROVED','Approved'),
        ('REJECTED','Rejected')
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE,related_name='tasks')
    title = models.CharField(max_length=150)
    description = models.TextField()
    deadline = models.DateField(blank=True,null=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='task_assigned')
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='task_created')
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} ({self.status})"
    
class TaskApproval(models.Model):
    ACTIONS_CHOICE= (
        ('APPROVED','Approved'),
        ('REJECTED','Rejected')
    )
    task = models.ForeignKey(Task, on_delete=models.CASCADE,related_name='approvals')
    
    action_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='task_approvals')
    action = models.CharField(max_length=10,choices=ACTIONS_CHOICE  )
    comment = models.TextField(blank=True) 
    action_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.task.title} - {self.action}"