from django.db import models
from django.utils import timezone
import random
import string

# Function to get or create the default motorcycle
def get_default_motorcycle():
    motorcycle, created = Motorcycle.objects.get_or_create(model='Välj MC')
    return motorcycle.id

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
    booking_start_date = models.DateField()
    booking_end_date = models.DateField()
    pickup_time = models.TimeField()
    dropoff_time = models.TimeField()
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    booking_message = models.TextField(blank=True, null=True)
    booking_id = models.CharField(max_length=5, unique=True, editable=False)
    payment_done = models.BooleanField(default=False, verbose_name="Payment Done")
    price = models.IntegerField(default=0, verbose_name="Total Price (SEK)")

    def calculate_price(self):
        """Calculate price based on number of days and discount rules."""
        days = (self.booking_end_date - self.booking_start_date).days + 1
        # Get base price per day depending on service
        if self.service_id and self.motorcycle_id:
            if self.service_id == 1:  # Adjust service_id as needed
                price_per_day = self.motorcycle.price_rent_1d
            elif self.service_id == 2:
                price_per_day = self.motorcycle.price_practise_1d
            elif self.service_id == 3:
                price_per_day = self.motorcycle.price_test
            else:
                price_per_day = 0
        else:
            price_per_day = 0

        # Fetch discount config (use defaults if not set)
        try:
            config = BookingDiscountConfig.objects.first()
            discount_3_to_6 = config.discount_3_to_6_days if config else 0.9
            discount_7_or_more = config.discount_7_or_more_days if config else 0.8
        except Exception:
            discount_3_to_6 = 0.9
            discount_7_or_more = 0.8

        total = price_per_day * days
        if 3 <= days <= 6:
            total = int(total * discount_3_to_6)
        elif days >= 7:
            total = int(total * discount_7_or_more)
        return total
    
    def generate_booking_id(self):
        """Generate a unique 5-letter booking ID"""
        while True:
            # Generate a random 5-letter string
            new_id = ''.join(random.choices(string.ascii_uppercase, k=5))
            # Check if it's unique
            if not Booking.objects.filter(booking_id=new_id).exists():
                return new_id

    def save(self, *args, **kwargs):
        # Generate booking_id if it doesn't exist
        if not self.booking_id:
            self.booking_id = self.generate_booking_id()
        # Set price if not manually set
        if not self.price or self.price == 0:
            self.price = self.calculate_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return (
        f"Booking {self.booking_id} of {self.motorcycle} by {self.first_name} {self.last_name} "
        f"for {self.service} from {self.booking_start_date} to {self.booking_end_date} "
        f"({self.pickup_time}–{self.dropoff_time})"
    )
    
    def is_active(self):
        return self.status in ['PENDING', 'CONFIRMED']

class BookingDiscountConfig(models.Model):
    discount_3_to_6_days = models.FloatField(default=0.9, verbose_name="3–6 days ratio")
    discount_7_or_more_days = models.FloatField(default=0.8, verbose_name="7+ days ratio")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Booking Discount Configuration"

    class Meta:
        verbose_name = "Booking Discount Config"
        verbose_name_plural = "Booking Discount Configs"

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