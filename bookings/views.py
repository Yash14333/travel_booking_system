from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.utils import timezone
from django.core.paginator import Paginator
from .models import TravelOption, Booking
from .forms import RegisterForm, ProfileForm, BookingForm
import uuid

def home(request):
    qs = TravelOption.objects.all()
    t = request.GET.get('type')
    src = request.GET.get('source')
    dst = request.GET.get('destination')
    date = request.GET.get('date')

    if t:
        qs = qs.filter(type=t)
    if src:
        qs = qs.filter(source__icontains=src)
    if dst:
        qs = qs.filter(destination__icontains=dst)
    if date:
        qs = qs.filter(departure_datetime__date=date)

    paginator = Paginator(qs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    ctx = {'page_obj': page_obj, 'type': t or '', 'source': src or '', 'destination': dst or '', 'date': date or ''}
    return render(request, 'home.html', ctx)

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})

def travel_detail(request, pk):
    travel = get_object_or_404(TravelOption, pk=pk)
    return render(request, 'travel_detail.html', {'travel': travel})

@login_required
@transaction.atomic
def book_travel(request, pk):
    travel = get_object_or_404(TravelOption, pk=pk)
    if request.method == "POST":
        form = BookingForm(request.POST, travel_option=travel)
        if form.is_valid():
            seats = form.cleaned_data['number_of_seats']
            if seats > travel.available_seats:
                form.add_error('number_of_seats', "Not enough seats available.")
            else:
                travel.available_seats -= seats
                travel.save()
                booking = Booking.objects.create(
                    booking_id=str(uuid.uuid4())[:8].upper(),
                    user=request.user,
                    travel_option=travel,
                    number_of_seats=seats,
                    total_price=seats * travel.price,
                    status='CONFIRMED'
                )
                messages.success(request, f"Booking confirmed! ID: {booking.booking_id}")
                return redirect('my_bookings')
    else:
        form = BookingForm(travel_option=travel)
    return render(request, 'book_travel.html', {'travel': travel, 'form': form})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).select_related('travel_option')
    now = timezone.now()
    current = bookings.filter(status='CONFIRMED', travel_option__departure_datetime__gte=now)
    past = bookings.filter(travel_option__departure_datetime__lt=now) | bookings.filter(status='CANCELLED')
    return render(request, 'my_bookings.html', {'current': current, 'past': past})

@login_required
@transaction.atomic
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    if booking.status == 'CANCELLED':
        messages.info(request, 'Booking already cancelled.')
    else:
        booking.status = 'CANCELLED'
        booking.save()
        travel = booking.travel_option
        travel.available_seats += booking.number_of_seats
        travel.save()
        messages.success(request, 'Booking cancelled and seats released.')
    return redirect('my_bookings')
