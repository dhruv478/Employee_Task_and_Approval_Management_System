from django.contrib import admin
from .models import Task
# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id','title','project','status','assigned_to','assigned_by')
    list_filter = ('status','project')
    
class TaskAdminApprovals(admin.ModelAdmin):
    list_display = ('id','task','action','action_by','action_date')
    list_filter = ('action')
    