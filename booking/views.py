from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import BookingForm, ContactForm, ReviewForm
from .models import Booking, ContactMessage, Review, Motorcycle
from datetime import datetime, time, timedelta, date
from django.core.mail import send_mail
import json

def home(request):
    reviews = Review.objects.filter(is_approved=True).order_by('-created_at')  # Only get approved reviews
    return render(request, 'bookings/home.html', {'reviews': reviews})

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

def get_booked_dates_for_motorcycle(motorcycle_id):
    # Get all active bookings for this motorcycle
    bookings = Booking.objects.filter(
        motorcycle_id=motorcycle_id,
        booking_date__gte=datetime.now().date(),
        status__in=['PENDING', 'CONFIRMED']
    ).values_list('booking_date', flat=True)
    
    # Convert dates to string format
    return [booking.strftime('%Y-%m-%d') for booking in bookings]


def create_booking(request):
    pickup_timeslots = generate_timeslots(time(7, 0), time(22, 0), 30)  # 9 AM to 5 PM for pickup
    dropoff_timeslots = generate_timeslots(time(7, 0), time(22, 0), 30)  # Same range for dropoff
    
    # Get all motorcycles
    motorcycles = Motorcycle.objects.all()
    
    # Get booked dates for each motorcycle
    booked_dates = {}
    for motorcycle in motorcycles:
        booked_dates[str(motorcycle.id)] = get_booked_dates_for_motorcycle(motorcycle.id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Check if the selected date is available
            selected_date = form.cleaned_data['booking_date']
            selected_motorcycle = form.cleaned_data['motorcycle']
            
            # Convert selected_date to string format for comparison
            date_str = selected_date.strftime('%Y-%m-%d')
            
            if date_str in booked_dates.get(str(selected_motorcycle.id), []):
                form.add_error('booking_date', 'This date is already booked for the selected motorcycle.')
            else:
                form.save()
                return redirect('booking_success')
    else:
        form = BookingForm()

    context = {
        'form': form,
        'pickup_timeslots': pickup_timeslots,
        'dropoff_timeslots': dropoff_timeslots,
        'booked_dates': json.dumps(booked_dates),  # Serialize the dates to JSON
        'motorcycles': {str(m.id): {
            'model': m.model,
            'booked_dates': booked_dates[str(m.id)]
        } for m in motorcycles}
    }

    return render(request, 'bookings/create_booking.html', context)  # Return the full context


def contact_submit(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Save the message to the database

            # Send an email notification
            send_mail(
                subject=f"New Contact Form Submission from {form.cleaned_data['name']}",
                message=f"Message: {form.cleaned_data['message']}\nPhone: {form.cleaned_data['phone']}\nEmail: {form.cleaned_data['email']}",
                from_email=form.cleaned_data['email'],
                recipient_list=['benny@hotmail.se'],
            )

            return redirect('contact_success')  # Redirect to a success page or message
    else:
        form = ContactForm()

    return render(request, 'bookings/contact.html', {'form': form})

def contact_success_view(request):
    return render(request, 'bookings/contact_success.html')

def add_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            # Populate fields from form data
            review.first_name = form.cleaned_data['first_name']
            review.last_name = form.cleaned_data['last_name']
            review.motorcycle = form.cleaned_data['motorcycle']
            review.rating = form.cleaned_data['rating']
            review.review_text = form.cleaned_data['review_text']
            review.save()
            return redirect('home')  # Redirect to the home page after submitting the review
    else:
        form = ReviewForm()
    
    return render(request, 'bookings/add_review.html', {'form': form})