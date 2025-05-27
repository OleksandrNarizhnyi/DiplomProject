from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import status, filters
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response

from booking.models.rent import Rental
from booking.permissions.custom_permissions import IsRentalOwnerOrReadOnly
from booking.serializers.rent import (
    RentalListSerializer,
    RentalCreateUpdateSerializer,
    )
from booking.utils.filters import RentalFilter


class RentalListCreateView(ListCreateAPIView):
    queryset = Rental.objects.select_related(
        'address', 'lessor'
    ).filter(
        deleted=False,
        is_active=True,
    )
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_class = RentalFilter
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RentalListSerializer
        return RentalCreateUpdateSerializer


class RentalRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Rental.objects.all()
    permission_classes = [IsRentalOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RentalListSerializer
        return RentalCreateUpdateSerializer

    def partial_update(self, request, *args, **kwargs):
        data = request.data
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)