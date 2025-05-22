from django.contrib import admin

from booking.models.review import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'rental', 'comment', 'rating')
    search_fields = ('rating',)
    list_filter = ('user', 'rental',)