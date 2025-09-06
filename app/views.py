from django.shortcuts import render
from django.http import JsonResponse

from app.models import Booking
from .forms import BookingForm
from django.core.mail import send_mail
from .forms import BookingForm
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import dns.resolver

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


def is_valid_email(email):
    """Check if the email is valid and has an existing domain."""
    try:
        validate_email(email)  # Validate email format
        domain = email.split('@')[1]  # Extract domain from email
        dns.resolver.resolve(domain, 'MX')  # Check if domain has MX records
        return True
    except (ValidationError, dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return False

def booking_view(request):
    if request.method == "POST":
        try:
            form = BookingForm(request.POST)
            print("Form Data:", request.POST)  # Debug print
            
            if form.is_valid():
                email = form.cleaned_data['email']
                
                # Basic email format validation
                if not email or '@' not in email:
                    return JsonResponse({
                        'errors': 'Please enter a valid email address.'
                    }, status=400)

                # Validate if the email is real
                if not is_valid_email(email):
                    return JsonResponse({
                        'errors': 'Invalid or non-existent email address. Please enter a correct email.'
                    }, status=400)

                service = form.cleaned_data['service']
                time = form.cleaned_data['time']
                date = form.cleaned_data['date']

                # Validate required fields
                if not all([service, time, date]):
                    return JsonResponse({
                        'errors': 'Please fill in all required fields.'
                    }, status=400)

                # Check if the same email has already booked the same service at the same time
                if Booking.objects.filter(email=email, service=service, time=time, date=date).exists():
                    return JsonResponse({
                        'errors': 'This email has already booked this service at this time.'
                    }, status=400)

                try:
                    # Save the booking
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
                    
                    https://wa.me/+918590884831?text=Hi%20I%20need%20assistance%20with%20my%20booking

                    Thank you for choosing our service!
                    """
                    try:
                        send_mail(
                            subject, 
                            message, 
                            settings.EMAIL_HOST_USER, 
                            [booking.email], 
                            fail_silently=True
                        )
                    except Exception as e:
                        print(f"Email sending failed: {str(e)}")  # Log email errors but don't fail the booking
                        
                    return JsonResponse({
                        'message': 'Booking successful!',
                        'redirect': '/'
                    }, status=200)
                    
                except Exception as e:
                    print(f"Booking save failed: {str(e)}")  # Debug print
                    return JsonResponse({
                        'errors': 'Unable to save your booking. Please try again.'
                    }, status=500)
            else:
                print("Form Errors:", form.errors)  # Debug print
                error_messages = {}
                for field, errors in form.errors.items():
                    error_messages[field] = [str(error) for error in errors]
                return JsonResponse({
                    'errors': error_messages
                }, status=400)
                
        except Exception as e:
            print(f"Unexpected error: {str(e)}")  # Debug print
            return JsonResponse({
                'errors': 'An unexpected error occurred. Please try again.'
            }, status=500)

    return render(request, 'booking.html')

