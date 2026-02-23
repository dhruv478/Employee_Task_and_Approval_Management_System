from rest_framework.permissions import BasePermission

# Permission: Allow only Admin or Manager users
class IsAdminOrManager(BasePermission):
    # This runs BEFORE entering the view
    # Used for general access control (e.g., creating projects)
    def has_permission(self, request, view):
        return (
            request.user                     # user must exist
            and request.user.is_authenticated # user must be logged in
            and request.user.role in ['ADMIN', 'MANAGER']  # role check
        )
# Permission: Allow only Admin users
class IsAdminOnly(BasePermission):
    # Only Admin role can access
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'ADMIN'
        )
# Permission: Object-level permission for Task
class IsTaskOwnerOrManager(BasePermission):
    # This runs AFTER the object is fetched
    # obj = Task instance
    def has_object_permission(self, request, view, obj):
        # Admin can access any task
        if request.user.role == 'ADMIN':
            return True

        # Manager can access any task
        if request.user.role == 'MANAGER':
            return True

        # Employee can only access their own task
        return obj.assigned_to == request.user