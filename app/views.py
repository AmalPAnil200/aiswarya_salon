from django.shortcuts import render
from django.http import JsonResponse

from app.models import Booking
from .forms import BookingForm
from django.core.mail import send_mail
from .forms import BookingForm
from django.conf import settings

def index_view(request):
    return render(request, 'index.html')

def home_view(request):
    return render(request, 'home.html')

def pricing_view(request):
    return render(request, 'pricing.html')

def media_view(request):
    return render(request, 'media.html')

def about_us_view(request):
    return render(request, 'about_us.html')

# def booking_view(request):
#     if request.method == "POST":
#         form = BookingForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return JsonResponse({'message': 'Booking successful!','redirect': '/'}, status=200)
#         else:
#             return JsonResponse({'errors': form.errors}, status=400)

#     return render(request, 'booking.html')


def booking_view(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            # Check if the booking already exists
            name = form.cleaned_data['name']
            service = form.cleaned_data['service']
            time = form.cleaned_data['time']
            date = form.cleaned_data['date']
            
            # If a booking exists with the same name, service, time, and date, prevent the booking
            if Booking.objects.filter(name=name, service=service, time=time, date=date).exists():
                return JsonResponse({'errors': 'You have already booked this service at this time.'}, status=400)
            
            # Save the new booking if it doesn't exist
            booking = form.save()

            # Send confirmation email
            subject = "Appointment Confirmation"
            message = f"""
            Dear {booking.name},

            Your booking has been confirmed!
            
            Details:
            - Service: {booking.service}
            - Date: {booking.date}
            - Time: {booking.time}
            
            If you have any questions, feel free to contact us.

            Thank you for choosing our service!
            """
            recipient_email = booking.email
            send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient_email], fail_silently=False)

            return JsonResponse({'message': 'Booking successful!', 'redirect': '/'}, status=200)
        else:
            return JsonResponse({'errors': form.errors}, status=400)

    return render(request, 'booking.html')
