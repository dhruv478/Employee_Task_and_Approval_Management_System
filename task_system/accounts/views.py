from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Project
from .serializers import ProjectSerializer
from .permissions import IsAdminOrManager


# ---------------------------
# 1️⃣ Identity Endpoint (/me)
# ---------------------------
# This API returns details of the currently logged-in user.
# It proves JWT authentication is working correctly.

class MeView(APIView):

    # Only authenticated users can access this endpoint
    permission_classes = [IsAuthenticated]

    # GET request returns user information
    def get(self, request):
        user = request.user  # Comes from JWTAuthentication
        return Response({
            "id": user.id,
            "username": user.username,
            "role": user.role
        })


# -----------------------------------
# 2️⃣ Project CRUD (ViewSet)
# -----------------------------------
# ModelViewSet provides:
# - list()
# - retrieve()
# - create()
# - update()
# - delete()

class ProjectViewSet(ModelViewSet):
    # Base queryset for projects
    queryset = Project.objects.all()
    # Serializer used to convert Project <-> JSON
    serializer_class = ProjectSerializer
    # User must be authenticated AND Admin/Manager
    permission_classes = [IsAuthenticated, IsAdminOrManager]

    # Automatically set created_by to logged-in user
    # Prevents frontend from faking project creator
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)