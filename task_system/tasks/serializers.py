from rest_framework import serializers
from .models import Task,TaskApproval

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task 
        fields = ['id','project','title','description','assigned_to','assigned_by','status','deadline','created_at','updated_at']
        read_only_fields = ['assigned_by','status','created_at','updated_at']
        
class TaskApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskApproval
        fields = ['id','task','action','comment','action_by','action_date']
        read_only_fields = ['action_by','action_date']