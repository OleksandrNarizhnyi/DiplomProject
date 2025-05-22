from booking.models.booking import Booking
from django.contrib import admin

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('rental', 'date_range', 'user', 'status_display')
    list_filter = ('is_confirmed', 'is_cancelled', 'rental')
    date_hierarchy = 'start_date'
    search_fields = ('rental__title',)

    def date_range(self, obj):
        return f"{obj.start_date} to {obj.end_date}"
    date_range.short_description = 'Booking Period'

    def status_display(self, obj):
        if obj.is_cancelled:
            return "Cancelled"
        return "Confirmed" if obj.is_confirmed else "Pending"
    status_display.short_description = 'Status'