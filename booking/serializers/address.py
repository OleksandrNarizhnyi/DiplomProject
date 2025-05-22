from rest_framework import serializers

from booking.models.address import Address


class AddressInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'land',
            'city',
            'street',
            'haus_num',
        ]