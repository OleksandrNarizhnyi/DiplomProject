from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsRentalOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.role == 'LESSOR' and request.user == obj.lessor


class IsRenter(BasePermission):
    message = "Only users with RENTER role can perform this action"

    def has_permission(self, request, view):
        return request.user.role == "RENTER"


class IsLessor(BasePermission):
    message = "Only users with LESSOR role can perform this action"

    def has_permission(self, request, view):
        return request.user.role == "LESSOR"


class IsBookingOwner(BasePermission):
    message = "You can only manage your own bookings"

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsPropertyLessor(BasePermission):
    message = "You can only manage bookings for your own properties"

    def has_object_permission(self, request, view, obj):
        return obj.rental.lessor == request.user