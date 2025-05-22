from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from booking.models.rent import Rental
from booking.serializers.address import AddressInfoSerializer


class RentalListSerializer(serializers.ModelSerializer):
    address = AddressInfoSerializer()

    lessor = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Rental
        fields = [
            'id', 'title', 'description', 'address',
            'room_count', 'room_type', 'price',
            'lessor', 'created_at',  'updated_at',

        ]
        read_only_fields = fields


class RentalCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = [
            'title', 'description', 'address',
            'price', 'room_count', 'room_type'
        ]
        extra_kwargs = {
            'address': {'required': True},
            'title': {'required': True},
            'description': {'required': True},
            'price': {'required': True},
            'room_count': {'required': True},
            'room_type': {'required': True},
        }

    def validate(self, attrs):
        request = self.context.get('request')

        if self.instance is None and request.user.role != 'LESSOR':
            raise PermissionDenied("Only users with the role 'LESSOR'  can create rental objects")

        if self.instance and self.instance.lessor != request.user:
            raise PermissionDenied("You can only edit your objects")

        return attrs

    def create(self, validated_data):
        validated_data['lessor'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.updated_at = timezone.now()
        return super().update(instance, validated_data)