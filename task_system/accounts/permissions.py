from rest_framework.permissions import BasePermission

class IsAdminOrManager(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated 
            and request.user.role in ['ADMIN','MANAGER']
        )

class IsAdminOnly(BasePermission):
    def has_permission(self, request, view):
        return super(
            request.user.is_authenticated and 
            request.user.role == 'ADMIN'
        )

class IsTaskOwnerOrManager(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'ADMIN':
            return True
        if request.user.role == 'MANAGER':
            return True
        
        return obj.assigned_to == request.user