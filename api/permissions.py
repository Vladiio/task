from rest_framework import permissions


class ReadUpdateDeletePerm(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == 'POST'
