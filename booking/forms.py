# booking/forms.py

from django import forms
from .models import Booking, Motorcycle

class BookingForm(forms.ModelForm):
    motorcycle = forms.ModelChoiceField(queryset=Motorcycle.objects.all(), label="Select Motorcycle")
    class Meta:
        model = Booking
        fields = ['name', 'email', 'motorcycle', 'service', 'booking_date', 'booking_time']
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date'}),
            'booking_time': forms.TimeInput(attrs={'type': 'time'}),
        }
