# bookings/admin.py

from django.contrib import admin
from .models import Booking, Motorcycle

# Register your models here
admin.site.register(Booking)
admin.site.register(Motorcycle)
