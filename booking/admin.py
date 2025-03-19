# bookings/admin.py

from django.contrib import admin
from .models import Booking, Motorcycle, Service, ContactMessage, Review

# Register your models here
admin.site.register(Motorcycle)
admin.site.register(Service)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'status', 'payment_done', 'first_name', 'last_name', 'motorcycle', 'service', 'booking_date', 'pickup_time', 'dropoff_time', 'created_at', 'phone_number', 'email')
    list_filter = ('status', 'payment_done', 'motorcycle', 'service', 'booking_date')
    search_fields = ('booking_id', 'first_name', 'last_name', 'email')
    readonly_fields = ('booking_id', 'created_at')  # Make booking_id read-only in detail view
    list_editable = ['payment_done']  # Allow editing payment status directly in list view

    fieldsets = (
        ('Booking Information', {
            'fields': ('booking_id', 'status', 'payment_done', 'created_at')
        }),
        ('Customer Details', {
            'fields': ('first_name', 'last_name', 'phone_number', 'email')
        }),
        ('Reservation Details', {
            'fields': ('motorcycle', 'service', 'booking_date', 'pickup_time', 'dropoff_time')
        }),
        ('Additional Information', {
            'fields': ('booking_message',)
        }),
    )

# Register the ContactMessage model to appear in the admin interface
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'subject', 'message','created_at')
    search_fields = ('name', 'phone', 'email', 'subject')
    list_filter = ('name', 'phone', 'email', 'created_at')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'motorcycle', 'rating', 'review_text', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'rating', 'motorcycle', 'created_at')
    search_fields = ('first_name', 'last_name,' 'review_text')
    actions = ['approve_reviews']

    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
    approve_reviews.short_description = 'Approve selected reviews'