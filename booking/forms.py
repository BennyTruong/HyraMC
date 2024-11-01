# booking/forms.py

from django import forms
from .models import Booking
from .models import ContactMessage
from .models import Review

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'motorcycle', 'service', 'booking_date', 'pickup_time', 'dropoff_time', 'booking_message']
        labels = {'first_name': 'Förnamn',
                  'last_name': 'Efternamn',
                  'phone_number': 'Telefonnummer',
                  'email': 'E-mail',
                  'motorcycle': 'Motorcykel',
                  'service': 'Hyrning',
                  'booking_date': 'Datum för hyra',
                  }
        widgets = {
            'booking_date': forms.DateInput(attrs={'id': 'datepicker', 'type': 'text'}),
            'pickup_time': forms.HiddenInput(),  # Pickup time will be selected via buttons
            'dropoff_time': forms.HiddenInput(),  # Dropoff time will be selected via buttons
            'booking_message': forms.Textarea(attrs={
                'placeholder': 'Eventuellt meddelande...',
                'rows': 4,
                'style': 'width:100%;',
            }),
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'phone', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ditt namn', 'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Ditt telefonnummer', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Din e-postadress', 'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Ämne för meddelandet', 'class': 'form-control'}),
            'message': forms.Textarea(attrs={'placeholder': 'Skriv ditt meddelande här...', 'class': 'form-control', 'rows': 4}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['first_name', 'last_name', 'motorcycle', 'rating', 'review_text']
        labels = {
            'first_name': 'Förnamn',
            'last_name': 'Efternamn (kommer inte visas för andra)',
            'motorcycle': 'Motorcykel du hyrde',
            'rating': 'Betyg',
            'review_text': 'Kommentar',
        }