from datetime import timedelta

from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework import status, filters
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes

from booking.models.booking import Booking
from booking.serializers.booking import BookingListSerializer, BookingCreateUpdateSerializer
from booking.permissions.custom_permissions import IsRenter, IsLessor, IsBookingOwner, IsPropertyLessor

class BookingListCreateView(ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return BookingListSerializer
        return BookingCreateUpdateSerializer

    def get_permissions(self):
        if self.request.method == 'PATCH':
            return [permission() for permission in [IsAuthenticated, IsRenter]]
        return [permission() for permission in [IsAuthenticated]]


    def get_queryset(self):
        queryset = Booking.objects.all()
        user = self.request.user

        if user.role == "RENTER":
            return queryset.filter(user=user)
        elif user.role == "LESSOR":
            return queryset.filter(rental__lessor=user)
        elif user.role == "ADMIN":
            return queryset
        return queryset.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BookingRetrieveUpdateView(RetrieveUpdateAPIView):
    queryset = Booking.objects.all()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return BookingListSerializer
        return BookingCreateUpdateSerializer

    def get_permissions(self):
        if self.request.method == 'PATCH':
            return [IsAuthenticated(), IsBookingOwner()]
        return [IsAuthenticated()]

    def perform_update(self, serializer):
        if 'is_cancelled' in serializer.validated_data and serializer.validated_data['is_cancelled']:
            instance = self.get_object()
            if instance.is_confirmed:
                raise ValidationError(
                    {"detail": "Cannot cancel already confirmed booking"}
                )
            if (instance.start_date - timezone.now().date()) <= timedelta(days=3):
                raise ValidationError(
                    {"detail": "Cancellation is only possible 3+ days before check-in"}
                )
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        data = request.data
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsLessor, IsPropertyLessor])
def confirm_booking(request, pk):
    booking = Booking.objects.get(pk=pk)
    booking.is_confirmed = True
    booking.is_cancelled = False
    booking.save()
    return Response({"status": "confirmed"}, status=status.HTTP_200_OK)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsLessor, IsPropertyLessor])
def reject_booking(request, pk):
    booking = Booking.objects.get(pk=pk)
    booking.is_confirmed = False
    booking.is_cancelled = True
    booking.save()
    return Response({"status": "rejected"}, status=status.HTTP_200_OK)

