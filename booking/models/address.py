from django.db import models

from booking.choices.choice_land import GermanState

class Address(models.Model):
    country = models.CharField(
        max_length=20,
        default="Deutschland",
        editable=False,
    )
    land = models.CharField(
        max_length=20,
        choices=GermanState.choices()
    )
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    haus_num = models.PositiveSmallIntegerField()
    apartment = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return f"Stadt {self.city}, str.{self.street[0:5]}."
