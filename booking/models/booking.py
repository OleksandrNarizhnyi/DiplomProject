from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

from booking.models import User
from booking.models.rent import Rental


class Booking(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='bookings',
        verbose_name='Renter'
    )
    rental = models.ForeignKey(
        Rental,
        on_delete=models.PROTECT,
        related_name='bookings',
        verbose_name='Rental Property'
    )
    start_date = models.DateField(verbose_name='Check-in Date')
    end_date = models.DateField(verbose_name='Check-out Date')
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Total Cost'
    )
    is_confirmed = models.BooleanField(default=False, verbose_name='Confirmed')
    is_cancelled = models.BooleanField(default=False, verbose_name='Cancelled')
    booked = models.BooleanField(default=False, verbose_name='Booked')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        status = "Pending"
        if self.is_cancelled:
            status = "Cancelled"
        elif self.is_confirmed:
            status = "Confirmed"
        elif self.booked:
            status = "Booked"
        return f"Booking #{self.id} - {self.rental.title} ({status})"

    def clean(self):
        if self.end_date <= self.start_date:
            raise ValidationError("Check-out date must be after check-in date.")

        if self.start_date < timezone.now().date():
            raise ValidationError("Cannot book in the past.")

        if not self.is_cancelled and self.booked:
            overlapping_bookings = Booking.objects.filter(
                rental=self.rental,
                start_date__lt=self.end_date,
                end_date__gt=self.start_date,
                is_cancelled=False
            ).exclude(pk=self.pk)

            if overlapping_bookings.exists():
                raise ValidationError("This property is already booked for the selected dates.")

    def save(self, *args, **kwargs):
        if not self.pk or 'start_date' in kwargs or 'end_date' in kwargs:
            nights = (self.end_date - self.start_date).days
            self.total_price = self.rental.price * nights

        if self.is_confirmed and not self.is_cancelled:
            self.booked = True
        else:
            self.booked = False

        if self.is_confirmed and self.is_cancelled:
            self.is_confirmed = False
            self.booked = False

        super().save(*args, **kwargs)

    class Meta:
        db_table = "booking"
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"
        ordering = ("-created_at",)
