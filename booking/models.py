from django.db import models
from django.utils import timezone

class Booking(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    service = models.CharField(max_length=200)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Booking by {self.name} for {self.service} on {self.booking_date} at {self.booking_time}"

