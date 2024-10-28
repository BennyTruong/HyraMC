# bookings/admin.py

from django.contrib import admin
from .models import Booking, Motorcycle, Service, ContactMessage

# Register your models here
admin.site.register(Booking)
admin.site.register(Motorcycle)
admin.site.register(Service)

# Register the ContactMessage model to appear in the admin interface
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')
    list_filter = ('created_at',)