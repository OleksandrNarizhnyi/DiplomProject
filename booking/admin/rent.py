from django.contrib import admin

from booking.models.rent import Rental

@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'address', 'price')
    search_fields = ('title', 'room_type')
    list_filter = ('price',)
    list_per_page = 10