from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from booking.models import User
from booking.models.rent import Rental
from booking.models.review import Review


class ReviewListSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    rental = serializers.SlugRelatedField(
        slug_field='title',
        read_only=True,
    )

    class Meta:
        model = Review
        fields = [
            'id', 'user', 'rental', 'booking',
            'rating', 'comment', 'created_at',
        ]
        read_only_fields = fields


class ReviewCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'id', 'user', 'rental', 'booking',
            'rating', 'comment', 'created_at',
        ]

    def validate_rating(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value

    def validate_booking(self, value):
        request = self.context.get('request')
        if value and value.user != request.user:
            raise serializers.ValidationError("You can only use your own bookings")
        return value

    def validate(self, attrs):
        request = self.context.get('request')
        rental = attrs.get('rental', getattr(self.instance, 'rental', None))
        booking = attrs.get('booking', getattr(self.instance, 'booking', None))

        if self.instance is None and request.user.role != 'RENTER':
            raise PermissionDenied("Only users with the role 'RENTER' can create reviews")

        if self.instance and self.instance.user != request.user:
            raise PermissionDenied("You can only edit your reviews")

        if booking and booking.rental != rental:
            raise serializers.ValidationError(
                {"booking": "Booking must be for the same rental as the review"}
            )

        return attrs

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
