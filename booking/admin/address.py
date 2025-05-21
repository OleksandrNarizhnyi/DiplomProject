from django.contrib import admin

from booking.models.address import Address

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('country', 'city', 'street', 'haus_num')
    search_fields = ('city',)
    list_filter = ('street',)
