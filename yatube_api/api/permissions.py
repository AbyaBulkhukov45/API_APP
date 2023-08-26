from rest_framework import permissions


class OwnerOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.method == 'POST'
            or (request.method in ['PUT', 'PATCH', 'DELETE']
                and obj.author == request.user)
        )
