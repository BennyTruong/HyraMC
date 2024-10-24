# bookings/admin.py

from django.contrib import admin
from .models import Booking, Motorcycle, Service

# Register your models here
admin.site.register(Booking)
admin.site.register(Motorcycle)
admin.site.register(Service)