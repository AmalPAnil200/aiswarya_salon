from django.shortcuts import redirect, render
from app.forms import BookingForm
from app.models import Booking
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from app.models import Booking
from django.views.decorators.csrf import csrf_exempt
import openpyxl
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils.timezone import now
from django.utils.timezone import localdate
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to the dashboard after successful login.
            return redirect('dashboard')
        else:
            error_message = "Invalid username or password."
            return render(request, 'admin_templates/login_admin.html', {'error_message': error_message})
    return render(request, 'admin_templates/login_admin.html')


def admin_logout(request):
    logout(request)
    return redirect('admin_login')


@login_required(login_url='/aiswaryaadmin/login_admin/')
def dashboard(request):
    # Count all appointments
    total_appointments = Booking.objects.count()
    # Get the last 5 bookings (or adjust as needed)
    recent_bookings = Booking.objects.order_by('-date')[:5]
    # Count all customers

    # Debug print (check your console)
    print("Total appointments:", total_appointments)
    
    return render(request, 'admin_templates/dashboard.html', {
        'total_appointments': total_appointments,
        'recent_bookings': recent_bookings,
    })


@login_required(login_url='/aiswaryaadmin/login_admin/')
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
                booking.status = "Cancelled"  # Instead of deleting, update the status
                message = f"Dear {booking.name},\n\nYour booking for {booking.service} on {booking.date} at {booking.time} has been CANCELLED.\n\nBest Regards,\nSalon Team"
            else:
                booking.date = new_date
                booking.time = new_time
                booking.status = "Rescheduled"
                message = f"Dear {booking.name},\n\nYour booking for {booking.service} has been rescheduled to {new_date} at {new_time}.\n\nBest Regards,\nSalon Team"

            booking.save()  # Save the updated booking instead of deleting

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



def export_appointments_xlsx(request):
    """Exports recent appointments to an Excel file."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Appointments"

    # Define headers
    headers = ["Client", "Service", "Date", "Time"]
    ws.append(headers)

    # Fetch recent bookings
    recent_bookings = Booking.objects.all().order_by('-date')[:10]  # Adjust query as needed

    # Add data to rows
    for booking in recent_bookings:
        ws.append([
            booking.name,
            booking.service,
            booking.date.strftime("%Y-%m-%d"),
            booking.time.strftime("%I:%M %p"),
        ])

    # Set response to download file
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = 'attachment; filename="appointments.xlsx"'
    wb.save(response)
    return response


def export_appointments_pdf(request):
    """Exports recent appointments to a PDF file."""
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="appointments.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, height - 50, "Recent Appointments")

    p.setFont("Helvetica", 12)
    y_position = height - 100
    headers = ["Client", "Service", "Date", "Time"]
    p.drawString(50, y_position, " | ".join(headers))
    y_position -= 20

    recent_bookings = Booking.objects.all().order_by('-date')[:10]  # Adjust query as needed

    for booking in recent_bookings:
        row = f"{booking.name} | {booking.service} | {booking.date.strftime('%Y-%m-%d')} | {booking.time.strftime('%I:%M %p')}"
        p.drawString(50, y_position, row)
        y_position -= 20

    p.showPage()
    p.save()
    return response



