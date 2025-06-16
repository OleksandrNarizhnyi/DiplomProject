from django_filters import rest_framework as filters
from booking.models.rent import Rental

class RentalFilter(filters.FilterSet):
    price_min = filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = filters.NumberFilter(field_name='price', lookup_expr='lte')
    rooms_min = filters.NumberFilter(field_name='room_count', lookup_expr='gte')
    rooms_max = filters.NumberFilter(field_name='room_count', lookup_expr='lte')
    city = filters.CharFilter(field_name='address__city', lookup_expr='icontains')
    land = filters.CharFilter(field_name='address__land', lookup_expr='icontains')
    room_type = filters.CharFilter(field_name='room_type', lookup_expr='exact')

    class Meta:
        model = Rental
        fields = []