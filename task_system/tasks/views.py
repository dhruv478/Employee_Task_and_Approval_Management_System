from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .models import Task, TaskApproval
from .serializers import TaskSerializer, TaskApprovalSerializer
from accounts.permissions import IsAdminOrManager, IsTaskOwnerOrManager

# -----------------------------------
# 1️⃣ Task ViewSet
# -----------------------------------
# Handles:
# - Create Task
# - List Tasks
# - Update Task
# - Delete Task
# - Submit Task (custom action)
class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    # User must be authenticated
    # Object-level permission handled by IsTaskOwnerOrManager
    permission_classes = [IsAuthenticated, IsTaskOwnerOrManager]
    # Filter tasks based on role
    def get_queryset(self):
        user = self.request.user
        # Admin & Manager can see all tasks
        if user.role in ['ADMIN', 'MANAGER']:
            return Task.objects.all()
        # Employee sees only assigned tasks
        return Task.objects.filter(assigned_to=user)

    # Automatically set assigned_by (Manager)
    def perform_create(self, serializer):
        serializer.save(assigned_by=self.request.user)
    # ---------------------------
    # Custom Action: Submit Task
    # URL: /api/tasks/<id>/submit/
    # ---------------------------
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        task = self.get_object()
        # Only assigned employee can submit
        if request.user != task.assigned_to:
            return Response(
                {"detail": "You cannot submit this task"},
                status=status.HTTP_403_FORBIDDEN
            )
        # Change task status
        task.status = 'SUBMITTED'
        task.save()

        return Response(
            {"detail": "Task submitted successfully"},
            status=status.HTTP_200_OK
        )
# -----------------------------------
# 2️⃣ Task Approval ViewSet
# -----------------------------------
# Handles approval / rejection of tasks
class TaskApprovalViewSet(ModelViewSet):
    serializer_class = TaskApprovalSerializer
    # Only Admin or Manager can approve/reject
    permission_classes = [IsAuthenticated, IsAdminOrManager]
    # All approvals visible to Admin/Manager
    def get_queryset(self):
        return TaskApproval.objects.all()
    # When approval is created:
    # - Save approval record
    # - Automatically update task status
    def perform_create(self, serializer):
        approval = serializer.save(action_by=self.request.user)
        task = approval.task
        # Update task status to APPROVED or REJECTED
        task.status = approval.action
        task.save()