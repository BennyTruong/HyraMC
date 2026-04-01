from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import BookingForm, ContactForm, ReviewForm
from .models import Booking, ContactMessage, Review, Motorcycle
from datetime import datetime, time, timedelta, date
from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
import json

def home(request):
    reviews = Review.objects.filter(is_approved=True).order_by('-created_at')  # Only get approved reviews
    return render(request, 'bookings/home.html', {'reviews': reviews})

def price(request):
    motorcycles = Motorcycle.objects.all().order_by('id')
    motorcycles = [motorcycles[1], motorcycles[0], motorcycles[2]] #Reorder to GSF600, GSF650, XL1000
    return render(request, 'bookings/price.html', {'motorcycles': motorcycles})

def contact(request):
    return render(request, 'bookings/contact.html')

def booking_success(request):
    has_pending = request.session.pop('has_pending', False)
    return render(request, 'bookings/booking_success.html', {
        'has_pending': has_pending
    })

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
    bookings = Booking.objects.filter(
        motorcycle_id=motorcycle_id,
        booking_end_date__gte=datetime.now().date(),
        status__in=['CONFIRMED']
    ).values_list('booking_start_date', 'booking_end_date')

    booked_days = []
    for start_date, end_date in bookings:
        current_date = start_date
        while current_date <= end_date:
            booked_days.append(current_date.strftime('%Y-%m-%d'))
            current_date += timedelta(days=1)
    return booked_days

def create_booking(request):
    pickup_timeslots = generate_timeslots(time(7, 0), time(22, 0), 30)  # 9 AM to 5 PM for pickup
    dropoff_timeslots = generate_timeslots(time(7, 0), time(22, 0), 30)  # Same range for dropoff
    motorcycles = Motorcycle.objects.all() # Get all motorcycles
    
    # Get booked dates for each motorcycle
    booked_dates = {}
    for motorcycle in motorcycles:
        booked_dates[str(motorcycle.id)] = get_booked_dates_for_motorcycle(motorcycle.id)
    
    # Create motorcycle prices dictionary
    motorcycle_prices = {
        str(m.id): {
            'model': m.model,
            'price_rent_1d': m.price_rent_1d,
            'price_practise_1d': m.price_practise_1d,
            'price_test': m.price_test,
            'available': m.availability_status
        } for m in motorcycles
    }

    context = {
        'form': BookingForm(),
        'pickup_timeslots': pickup_timeslots,
        'dropoff_timeslots': dropoff_timeslots,
        'booked_dates': json.dumps(booked_dates),
        'motorcycle_prices': json.dumps(motorcycle_prices, cls=DjangoJSONEncoder),
        'motorcycles': motorcycles,  # Keep this for form rendering
    }    

    if request.method == 'POST':
        form = BookingForm(request.POST)
        context['form'] = form  # Update form in context

        if form.is_valid():
            try:
                # Get the date and time values
                booking_start_date = request.POST.get('booking_start_date')
                booking_end_date = request.POST.get('booking_end_date')
                pickup_time = request.POST.get('pickup_time')
                dropoff_time = request.POST.get('dropoff_time')
                motorcycle_id = request.POST.get('motorcycle')

                if not all([booking_start_date, booking_end_date, pickup_time, dropoff_time]):
                    messages.error(request, 'Vänligen fyll i alla obligatoriska fält.')
                    return render(request, 'bookings/create_booking.html', context)

                # Check for pending bookings
                pending_booking = Booking.objects.filter(
                    motorcycle_id=motorcycle_id,
                    booking_start_date=datetime.strptime(booking_start_date, '%Y-%m-%d').date(),
                    booking_end_date=datetime.strptime(booking_end_date, '%Y-%m-%d').date(),
                    status='PENDING'
                ).exists()

                # Create booking but don't save yet
                booking = form.save(commit=False)
                
                try:
                    # Convert string dates to proper datetime objects
                    booking.booking_start_date = datetime.strptime(booking_start_date, '%Y-%m-%d').date()
                    booking.booking_end_date = datetime.strptime(booking_end_date, '%Y-%m-%d').date()
                    booking.pickup_time = datetime.strptime(pickup_time, '%H:%M').time()
                    booking.dropoff_time = datetime.strptime(dropoff_time, '%H:%M').time()
                except ValueError as e:
                    messages.error(request, 'Ogiltigt datum eller tidsformat.')
                    return render(request, 'bookings/create_booking.html', context)
                
                # Save the booking
                booking.save()
                
                # Store booking ID in session for success page
                request.session['booking_id'] = booking.booking_id
                request.session['has_pending'] = pending_booking

                # Store pending status in session
                request.session['has_pending'] = pending_booking

                messages.success(request, f'Bokning skapad! Ditt bokningsnummer är: {booking.booking_id}')
                return redirect('booking_success')

            except ValueError as e:
                messages.error(request, 'Ogiltigt datum eller tidsformat.')
                return render(request, 'bookings/create_booking.html', context)
    else:
        form = BookingForm()

    return render(request, 'bookings/create_booking.html', context)  # Return the full context


def contact_submit(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Save the message to the database
            
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

def rentalpolicy(request):
    return render(request, 'bookings/rentalpolicy.html')