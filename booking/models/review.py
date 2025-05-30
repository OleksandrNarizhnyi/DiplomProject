from django.db import models
from django.core.exceptions import ValidationError

from booking.models import User
from booking.models.booking import Booking
from booking.models.rent import Rental


class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='reviews'
    )
    rental = models.ForeignKey(
        Rental,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    booking = models.OneToOneField(
        Booking,
        on_delete=models.PROTECT,
        related_name='review',
    )
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    comment = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user} for {self.rental}"

    def clean(self):
        super().clean()

        if self.booking and (self.booking.user != self.user or self.booking.rental != self.rental):
            raise ValidationError("Booking must belong to the user and be for the same rental")

    class Meta:
        db_table = "review"
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        unique_together = ('user', 'rental')
        ordering = ("-created_at",)

