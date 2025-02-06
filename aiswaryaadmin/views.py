from django.shortcuts import redirect, render
from app.forms import BookingForm
from app.models import Appointment,Booking
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from app.models import Booking
from django.views.decorators.csrf import csrf_exempt

from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.

def dashboard(request):
    # Fetch the most recent bookings (you can modify this query based on your requirement)
    recent_bookings = Booking.objects.all().order_by('-created_at')[:5]  # Fetch the latest 5 bookings

    # Pass the bookings data to the template
    return render(request, 'admin_templates/dashboard.html', {'recent_bookings': recent_bookings})


def dashboard_base(request):
    return render(request, 'admin_templates/dashboard_base.html')

# def appointment(request):
#     bookings = Booking.objects.all().order_by('date', 'time')
#     return render(request, 'admin_templates/appointment.html', {'appointment': bookings})

# def delete_booking(request, booking_id):
#     if request.method == 'POST':
#         booking = get_object_or_404(Booking, id=booking_id)
#         booking.delete()
#         return redirect('appointment')
#     return HttpResponse(status=405)


def view_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    booking_details = {
        'name': booking.name,
        'service': booking.service,
        'date': booking.date.strftime('%Y-%m-%d'),
        'time': booking.time.strftime('%I:%M %p'),
        'phone': booking.phone,
        'email': booking.email,
        'special_requests': booking.special_requests,
    }

    return JsonResponse(booking_details)

@csrf_exempt  # Optional if CSRF token is included in the form
def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        try:
            new_date = request.POST.get('new_date')
            new_time = request.POST.get('new_time')
            cancel_booking = request.POST.get('cancel_booking') == 'on'  # Checkbox returns 'on' when checked

            subject = "Your Booking Update"
            message = ""

            if cancel_booking:
                message = f"Dear {booking.name},\n\nYour booking for {booking.service} on {booking.date} at {booking.time} has been CANCELLED.\n\nBest Regards,\nSalon Team"
                booking.delete()  # Delete booking if canceled
            else:
                booking.date = new_date
                booking.time = new_time
                booking.save()
                message = f"Dear {booking.name},\n\nYour booking for {booking.service} has been rescheduled to {new_date} at {new_time}.\n\nBest Regards,\nSalon Team"

            # Send Email
            send_mail(
                subject,
                message,
                'your-email@example.com',  # Change this to your actual email
                [booking.email],
                fail_silently=False,
            )

            return JsonResponse({"success": True, "message": "Notification sent successfully!"})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.delete()
    return redirect('dashboard')  # Redirect back to the appointment list after deletion

