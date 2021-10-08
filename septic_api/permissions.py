from rest_framework import permissions


class IsOwnerOrSuperUser(permissions.BasePermission):
    """
    Custom permission to only allow owners or admin of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the owner of the home or the admin.
        return (obj.owner == request.user) or (request.user.is_superuser)