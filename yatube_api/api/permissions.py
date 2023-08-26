from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import permissions


class IsAuthorOrReadOnly(BasePermission):
    message = 'У вас нет прав'

    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
            or request.method in SAFE_METHODS
        )


class OnlyGetPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return False


class OnlyGetPostPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allowed_methods = ['GET', 'POST']
        return request.method in allowed_methods
