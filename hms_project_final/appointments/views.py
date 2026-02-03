ssimport requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, SlotForm
from .models import Slot, Booking
from .calendar_utils import add_event_to_calendar

LAMBDA_EMAIL_URL = "http://localhost:3000/dev/send-email"

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            role = form.cleaned_data.get('role')
            
            if role == 'doctor':
                user.is_doctor = True
            else:
                user.is_patient = True
            user.save()

            # Trigger Welcome Email via Lambda
            try:
                requests.post(LAMBDA_EMAIL_URL, json={
                    "type": "SIGNUP_WELCOME",
                    "email": user.email,
                    "name": user.username
                }, timeout=5)
            except requests.exceptions.RequestException as e:
                print(f"Lambda Email Error: {e}")

            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def dashboard(request):
    if request.user.is_doctor:
        slots = Slot.objects.filter(doctor=request.user).order_by('start_time')
        form = SlotForm(request.POST or None)
        if request.method == 'POST' and form.is_valid():
            slot = form.save(commit=False)
            slot.doctor = request.user
            slot.save()
            return redirect('dashboard')
        return render(request, 'doctor_dashboard.html', {'slots': slots, 'form': form})
    else:
        available_slots = Slot.objects.filter(is_booked=False)
        my_bookings = Booking.objects.filter(patient=request.user)
        return render(request, 'patient_dashboard.html', {
            'slots': available_slots, 
            'bookings': my_bookings
        })

@login_required
def book_appointment(request, slot_id):
    slot = get_object_or_404(Slot, id=slot_id)
    
    if not slot.is_booked:
        # 1. Create the Database Record
        booking = Booking.objects.create(patient=request.user, slot=slot)
        slot.is_booked = True
        slot.save()

        # 2. Add to Google Calendar
        # We pass the usernames and emails to meet the requirement of dynamic titles
        try:
            calendar_link = add_event_to_calendar(
                doctor_name=slot.doctor.username,
                doctor_email=slot.doctor.email,
                patient_name=request.user.username,
                patient_email=request.user.email,
                start_time_str=slot.start_time.isoformat()
            )
            print(f"Calendar Event Created: {calendar_link}")
        except Exception as e:
            print(f"Google Calendar Error: {e}")

        # 3. Trigger Booking Confirmation via Lambda
        payload = {
            "type": "BOOKING_CONFIRMATION",
            "patient_email": request.user.email,
            "doctor_email": slot.doctor.email,
            "start_time": slot.start_time.strftime("%Y-%m-%d %H:%M"),
            "doctor_name": slot.doctor.username
        }
        
        try:
            requests.post(LAMBDA_EMAIL_URL, json=payload, timeout=5)
        except requests.exceptions.RequestException as e:
            print(f"Lambda Confirmation Error: {e}")

    return redirect('dashboard')
