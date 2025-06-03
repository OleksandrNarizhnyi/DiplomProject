from datetime import timedelta

from django.db.models import Q
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework import status, filters
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response

from booking.models.booking import Booking
from booking.serializers.booking import BookingListSerializer, BookingCreateUpdateSerializer
from booking.permissions.custom_permissions import IsBookingOwner, IsPropertyLessor

class BookingListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    filterset_fields = ['rental', 'start_date', 'end_date']
    search_fields = ['rental', 'start_date', 'end_date']
    ordering_fields = ['start_date', 'end_date']

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return BookingListSerializer
        return BookingCreateUpdateSerializer

    # def get_permissions(self):
    #     if self.request.method == 'PATH':
    #         return [permission() for permission in [IsAuthenticated, IsRenter]]
    #     return [permission() for permission in [IsAuthenticated]]


    def get_queryset(self):
        queryset = Booking.objects.select_related('user', 'rental__lessor')
        user = self.request.user

        if user.is_superuser:
            return queryset
        return queryset.filter(Q(user=user) | Q(rental__lessor=user))

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

class ConfirmBookingView(UpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingCreateUpdateSerializer
    permission_classes = [IsPropertyLessor]
    http_method_names = ['patch']

    def perform_update(self, serializer):
        serializer.save(is_confirmed=True, is_cancelled=False)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data={}, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"status": "confirmed"}, status=status.HTTP_200_OK)

class RejectBookingView(UpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingCreateUpdateSerializer
    permission_classes = [IsPropertyLessor]
    http_method_names = ['patch']

    def perform_update(self, serializer):
        serializer.save(is_confirmed=False, is_cancelled=True)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data={}, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"status": "rejected"}, status=status.HTTP_200_OK)

