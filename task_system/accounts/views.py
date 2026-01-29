from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Project
from .serializers import ProjectSerializer
from .permissions import IsAdminOrManager

class MeView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        user = request.user
        return Response({"id":user.id,"username":user.username,"role":user.role})
    
class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)