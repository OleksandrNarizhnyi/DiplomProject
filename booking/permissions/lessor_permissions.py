from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsRentalOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        print(request.user)
        return request.user.role == 'LESSOR' and request.user == obj.lessor

