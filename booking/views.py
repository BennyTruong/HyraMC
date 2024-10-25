from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import BookingForm
from .models import Booking
from datetime import datetime, time, timedelta, date

def home(request):
    return render(request, 'bookings/home.html')

def create_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('booking_success')
    else:
        form = BookingForm()
    return render(request, 'bookings/create_booking.html', {'form': form})

def price(request):
    return render(request, 'bookings/price.html')

def contact(request):
    return render(request, 'bookings/contact.html')

def booking_success(request):
    return render(request, 'bookings/booking_success.html')

def booking_list(request):
    bookings = Booking.objects.all()
    return render(request, 'bookings/booking_list.html', {'bookings': bookings})

def generate_timeslots(start_time, end_time, interval_minutes=60):
    timeslots = []
    current_time = start_time
    while current_time < end_time:
        timeslots.append(current_time.strftime('%H:%M'))  # Format as "HH:MM"
        current_time = (datetime.combine(date.today(), current_time) + timedelta(minutes=interval_minutes)).time()
    return timeslots

def create_booking(request):
    pickup_timeslots = generate_timeslots(time(9, 0), time(17, 0), 30)  # 9 AM to 5 PM for pickup
    dropoff_timeslots = generate_timeslots(time(9, 0), time(17, 0), 30)  # Same range for dropoff
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('booking_success')
    else:
        form = BookingForm()
    return render(request, 'bookings/create_booking.html', {
        'form': form, 
        'pickup_timeslots': pickup_timeslots,
        'dropoff_timeslots': dropoff_timeslots
    })