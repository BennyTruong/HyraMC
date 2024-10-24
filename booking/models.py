from django.db import models
from django.utils import timezone

class Motorcycle(models.Model):
    model = models.CharField(max_length=100)

    def __str__(self):
        return self.model

class Service(models.Model):
    service = models.CharField(max_length=100)

    def __str__(self):
        return self.service  # This will display the service name in the dropdown

# Function to get or create the default motorcycle
def get_default_motorcycle():
    motorcycle, created = Motorcycle.objects.get_or_create(model='Välj MC')
    return motorcycle.id
class Booking(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    motorcycle = models.ForeignKey(Motorcycle, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    booking_date = models.DateField()
    pickup_time = models.TimeField()
    dropoff_time = models.TimeField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Booking by {self.name} for {self.service} on {self.booking_date} from {self.pickup_time} to {self.dropoff_time}"

