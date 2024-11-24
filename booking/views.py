from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import BookingForm, ContactForm, ReviewForm
from .models import Booking, ContactMessage, Review
from datetime import datetime, time, timedelta, date
from django.core.mail import send_mail

def home(request):
    reviews = Review.objects.filter(is_approved=True).order_by('-created_at')  # Only get approved reviews
    return render(request, 'bookings/home.html', {'reviews': reviews})

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