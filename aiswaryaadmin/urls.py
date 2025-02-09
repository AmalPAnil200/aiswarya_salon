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

    path("export/xlsx/", views.export_appointments_xlsx, name="export_xlsx"),
    path("export/pdf/", views.export_appointments_pdf, name="export_pdf"),
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
]
