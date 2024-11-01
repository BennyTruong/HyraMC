from django.db import models
from django.utils import timezone

class Motorcycle(models.Model):
    model = models.CharField(max_length=100)
    price_rent_1d = models.IntegerField(default=0)  # Rental price per day
    price_practise_1d = models.IntegerField(default=0)  # Practise price per day
    price_test = models.IntegerField(default=0)  # Price for driving test
    availability_status = models.BooleanField(default=True)  # Availability status: True if available, False if not

    def __str__(self):
        return self.model
    
    def is_available(self):
        return self.availability_status

class Service(models.Model):
    service = models.CharField(max_length=100)

    def __str__(self):
        return self.service  # This will display the service name in the dropdown

# Function to get or create the default motorcycle
def get_default_motorcycle():
    motorcycle, created = Motorcycle.objects.get_or_create(model='Välj MC')
    return motorcycle.id
class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
        ('COMPLETED', 'Completed'),
    ]

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=25)
    email = models.EmailField()
    motorcycle = models.ForeignKey(Motorcycle, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    booking_date = models.DateField()
    pickup_time = models.TimeField()
    dropoff_time = models.TimeField()
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    booking_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Booking by {self.first_name} {self.last_name} for {self.service} on {self.booking_date} from {self.pickup_time} to {self.dropoff_time}"
    
    def is_active(self):
        return self.status in ['PENDING', 'CONFIRMED']
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.name} - {self.email}'
    
class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 - Dåligt'),
        (2, '2 - Inte bra'),
        (3, '3 - Okej'),
        (4, '4 - Bra'),
        (5, '5 - Utmärkt'),
    ]

    first_name = models.CharField(max_length=100)  # First name of the reviewer
    last_name = models.CharField(max_length=100)  # Last name of the reviewer
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    motorcycle = models.ForeignKey('Motorcycle', on_delete=models.CASCADE, related_name='reviews')  # Link to the rented motorcycle
    review_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_approved = models.BooleanField(default=False)  # Field to indicate if the review is approved

    def __str__(self):
        return f"Review by {self.first_name} {self.last_name} ({self.rating} hearts)"