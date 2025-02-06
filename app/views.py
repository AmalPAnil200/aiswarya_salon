from django.shortcuts import render

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

def booking_view(request):
    return render(request, 'booking.html')
