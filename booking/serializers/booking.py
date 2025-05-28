from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers

from booking.models import User
from booking.models.booking import Booking
from booking.models.rent import Rental


class BookingListSerializer(serializers.ModelSerializer):
    can_cancel = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.filter(role="RENTER").all(),
    )
    rental = serializers.SlugRelatedField(
        slug_field='title',
        queryset=Rental.objects.all(),
    )

    class Meta:
        model = Booking
        fields = [
            'id', 'user', 'rental', 'start_date',
            'end_date', 'total_price', 'is_confirmed',
            'is_cancelled', 'booked', 'can_cancel', 'status',
            'created_at', 'updated_at'
        ]
        read_only_fields = fields

    def get_can_cancel(self, obj):
        if obj.is_cancelled or obj.is_confirmed:
            return False
        return (obj.start_date - timezone.now().date()) > timedelta(days=3)

    def get_status(self, obj):
        if obj.is_cancelled:
            return 'cancelled'
        if obj.is_confirmed:
            return 'confirmed'
        return 'pending'


class BookingCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'id', 'rental', 'start_date', 'end_date',
            'total_price', 'is_confirmed', 'is_cancelled'
        ]
        read_only_fields = ['total_price',]

    def validate(self, data):
        if not self.instance:
            if 'rental' not in data:
                raise serializers.ValidationError(
                    {"rental": "Rental property is required"}
                )

            start_date = data['start_date']
            end_date = data['end_date']
            user = self.context['request'].user

            if start_date >= end_date:
                raise serializers.ValidationError(
                    {"dates": "Check-out date must be after check-in date"}
                )

            if start_date < timezone.now().date():
                raise serializers.ValidationError(
                    {"dates": "Cannot book for past dates"}
                )

            overlapping = Booking.objects.filter(
                rental=data['rental'],
                start_date__lt=end_date,
                end_date__gt=start_date,
                is_cancelled=False
            ).exists()
            if overlapping:
                raise serializers.ValidationError(
                    {"dates": "The property is already booked for these dates"}
                )

            user_overlapping = Booking.objects.filter(
                user=user,
                start_date__lt=end_date,
                end_date__gt=start_date,
                is_cancelled=False
            ).exists()
            if user_overlapping:
                raise serializers.ValidationError(
                    {"dates": "You already have an active booking for these dates"}
                )

        else:
            if 'is_confirmed' in data and data['is_confirmed'] != self.instance.is_confirmed:
                raise serializers.ValidationError(
                    {"confirmation": "Only lessor can confirm bookings"}
                )

            if 'is_cancelled' in data and data['is_cancelled']:
                if self.instance.is_confirmed:
                    raise serializers.ValidationError(
                        {"cancellation": "Cannot cancel already confirmed booking"}
                    )

                if (self.instance.start_date - timezone.now().date()).days <= 3:
                    raise serializers.ValidationError(
                        {"cancellation": "Cancellation is only possible 3+ days before check-in"}
                    )

        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        nights = (validated_data['end_date'] - validated_data['start_date']).days
        validated_data['total_price'] = validated_data['rental'].price * nights
        return super().create(validated_data)

