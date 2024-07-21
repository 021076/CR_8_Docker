from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwner(BasePermission):
    """ Разрешение только для владельцев"""

    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        return False


class ListIsPublicHabits(BasePermission):
    """ Разрешение на просмотр списка публичных привычек, если не владелец, то только чтение"""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return False
