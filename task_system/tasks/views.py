from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Task, TaskApproval
from .serializers import TaskSerializer, TaskApprovalSerializer
from accounts.permissions import IsAdminOrManager, IsTaskOwnerOrManager
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsTaskOwnerOrManager]
    
    def get_queryset(self):
        user = self.request.user
        if user.role in ['ADMIN','MANAGER']:
            return Task.objects.all()
        return Task.objects.filter(assigned_to=user)
    
    def perform_create(self, serializer):
        serializer.save(assigned_by=self.request.user)
        
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        task = self.get_object()
        
        if request.user != task.assigned_to:
            return Response(
                {"detail":"You cannot submit this task"},
                status = status.HTTP_403_FORBIDDEN
            )
        
        task.status = 'SUBMITTED'
        task.save()
        
        return Response({"details":"Task submitted succesfully"})
    
class TaskApprovalViewSet(ModelViewSet):
    serializer_class = TaskApprovalSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]
    
    def get_queryset(self):
        return TaskApproval.objects.all()
    
    def perform_create(self, serializer):
        approval = serializer.save(action_by=self.request.user)
        task = approval.task
        task.status = approval.action
        task.save()
        