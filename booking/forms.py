# booking/forms.py

from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'email', 'motorcycle', 'service', 'booking_date', 'pickup_time', 'dropoff_time']
        widgets = {
            'booking_date': forms.DateInput(attrs={'id': 'datepicker', 'type': 'text'}),
            'pickup_time': forms.HiddenInput(),  # Pickup time will be selected via buttons
            'dropoff_time': forms.HiddenInput(),  # Dropoff time will be selected via buttons
        }
