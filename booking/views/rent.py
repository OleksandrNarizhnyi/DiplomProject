from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListCreateAPIView
from rest_framework import status, filters
from rest_framework.permissions import SAFE_METHODS

from booking.models.rent import Rental
from booking.serializers.rent import (
    RentalListSerializer,
    RentalCreateUpdateSerializer,
    )


class RentalListCreateView(ListCreateAPIView):
    queryset = Rental.objects.select_related(
        'address', 'lessor'
    ).all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['address__land', 'address__city',]
    search_fields = ['title', 'description']
    ordering_fields = ['price']

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RentalListSerializer
        return RentalCreateUpdateSerializer