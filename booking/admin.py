# bookings/admin.py

from django.contrib import admin
from .models import Booking, Motorcycle, Service, ContactMessage, Review

# Register your models here
admin.site.register(Motorcycle)
admin.site.register(Service)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'motorcycle', 'service', 'booking_date', 'status', 'pickup_time', 'dropoff_time')
    list_filter = ('motorcycle', 'status', 'booking_date')
    search_fields = ('first_name', 'last_name', 'email')

# Register the ContactMessage model to appear in the admin interface
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'message','created_at')
    search_fields = ('name', 'email', 'subject')
    list_filter = ('created_at',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'motorcycle', 'rating', 'review_text', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'rating', 'created_at', 'motorcycle')
    search_fields = ('first_name', 'last_name,' 'review_text')
    actions = ['approve_reviews']

    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
    approve_reviews.short_description = 'Approve selected reviews'