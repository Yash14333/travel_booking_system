from django.contrib import admin
from .models import TravelOption, Booking

@admin.register(TravelOption)
class TravelOptionAdmin(admin.ModelAdmin):
    list_display = ('travel_id', 'type', 'source', 'destination', 'departure_datetime', 'price', 'available_seats')
    search_fields = ('travel_id', 'source', 'destination')
    list_filter = ('type',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'user', 'travel_option', 'number_of_seats', 'total_price', 'status', 'booking_date')
    list_filter = ('status',)
    search_fields = ('booking_id', 'user__username', 'travel_option__travel_id')
