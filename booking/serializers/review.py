from rest_framework import serializers

from booking.models import User
from booking.models.rent import Rental
from booking.models.review import Review


class ReviewListSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.filter(role="RENTER").all(),
    )
    rental = serializers.SlugRelatedField(
        slug_field='title',
        queryset=Rental.objects.all(),
    )

    class Meta:
        model = Review
        fields = [
            'id', 'user', 'rental', 'booking',
            'rating', 'comment', 'created_at',
        ]
        read_only_fields = fields
