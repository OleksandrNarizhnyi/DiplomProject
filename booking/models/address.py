from django.db import models

class Address(models.Model):
    country = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    street = models.CharField(max_length=30)
    haus_num = models.PositiveSmallIntegerField()
    apartment = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return f"Stadt {self.city}, str.{self.street[0:5]}."
