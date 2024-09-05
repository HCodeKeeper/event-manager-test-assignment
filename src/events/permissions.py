from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsEventOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow any user to read objects
        if request.method in SAFE_METHODS:
            return True
        # Allow owners to update or delete objects
        return obj.organizer == request.user
