from rest_framework import permissions


class IsAdminOrIsSelf(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        return obj == request.user or request.user.is_staff


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        return obj.owner == request.user


class IsOrderOwnerOrAdmin(permissions.BasePermission):

    """ An order has no FK to a user. This is on purpose so the user
    can be deleted at some stage and the order would still be in our
    database for reporting and accounting purposes. So the check is on the
    owner property.
    """

    def has_object_permission(self, request, view, obj):

        return obj.owner == request.user or request.user.is_staff
