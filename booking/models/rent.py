from django.db import models

from booking.choices.room_type import RoomType
from booking.models import User
from booking.models.address import Address


class Rental(models.Model):
    title = models.CharField(max_length=40)
    description = models.CharField(max_length=500)
    address = models.OneToOneField(
        Address,
        on_delete=models.PROTECT,
        related_name="rental",
    )
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2
    )
    room_count = models.PositiveSmallIntegerField()
    room_type = models.CharField(
        max_length=40,
        choices=RoomType.choices()
    )
    lessor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="rentals"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "rental"
        verbose_name = "Rental"
        verbose_name_plural = "Rentals"
        unique_together = ("title", "address")
        ordering = ("-created_at",)