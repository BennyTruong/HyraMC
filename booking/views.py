from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import BookingForm
from .models import Booking

def home(request):
    return HttpResponse("Hello, Django!")

def create_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('booking_success')
    else:
        form = BookingForm()
    return render(request, 'bookings/create_booking.html', {'form': form})

def booking_success(request):
    return render(request, 'bookings/booking_success.html')

def booking_list(request):
    bookings = Booking.objects.all()
    return render(request, 'bookings/booking_list.html', {'bookings': bookings})
