from rest_framework import permissions

class IsSuperUserOrReadOnly(permissions.BasePermission):
    """
    Allows read-only access to all, write access only for superusers.
    """

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_superuser


class IsVerifiedSellerOrReadOnly(permissions.BasePermission):
    """
    Allows read-only access to all, write access only to verified sellers who own the object.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (request.user.is_authenticated and
                hasattr(request.user, 'seller_profile') and
                request.user.seller_profile.is_verified)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.seller.user == request.user