from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, TaskApprovalViewSet

router = DefaultRouter()
router.register('task',TaskViewSet,basename='task')
router.register('approval',TaskApprovalViewSet,basename='approval')

urlpatterns = router.urls
