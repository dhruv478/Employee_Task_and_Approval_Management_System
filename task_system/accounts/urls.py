from django.urls import path
from .views import MeView, ProjectViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('projects',ProjectViewSet, basename='projects')

urlpatterns = [
    path('me/',MeView.as_view(),name='me'),
]

urlpatterns += router.urls