import requests
from django.db import transaction
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Slot
from .utils import create_google_calendar_event

class BookAppointmentView(APIView):
    def post(self, request, slot_id):
        # 1. Atomic Transaction to prevent Race Conditions
        with transaction.atomic():
            try:
                # select_for_update() locks the row until the 'with' block ends
                slot = Slot.objects.select_for_update().get(id=slot_id, is_booked=False)
            except Slot.DoesNotExist:
                return Response({"error": "Slot already booked or doesn't exist"}, status=400)

            # 2. Update Slot
            slot.patient = request.user
            slot.is_booked = True
            slot.save()

        # 3. Call Serverless Email Lambda
        try:
            requests.post(
                settings.LAMBDA_URL, 
                json={"type": "BOOKING", "email": request.user.email}
            )
        except Exception as e:
            print(f"Lambda failed: {e}")

        # 4. Create Google Calendar Event
        # This requires the user's OAuth tokens (stored in their profile)
        calendar_link = create_google_calendar_event(request.user, slot)

        return Response({
            "message": "Appointment booked successfully!",
            "calendar_link": calendar_link
        })
