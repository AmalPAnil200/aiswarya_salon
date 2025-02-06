from django.urls import path
from aiswaryaadmin import views  # Ensure you have views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard_base/', views.dashboard_base, name='dashboard_base'),
    # path('appointment/', views.appointment, name='appointment'),
    # path('bookings/<int:booking_id>/delete/', views.delete_booking, name='delete_booking'),

    path('bookings/<int:booking_id>/view/', views.view_booking, name='view_booking'),
    path('bookings/<int:booking_id>/edit/', views.edit_booking, name='edit_booking'),
    path('bookings/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
]
