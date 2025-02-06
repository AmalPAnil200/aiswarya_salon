from django.db import models

class Booking(models.Model):
    SERVICE_CHOICES = [
        ('Haircut', 'Haircut'),
        ('Hair Color', 'Hair Color'),
        ('Spa Treatment', 'Spa Treatment'),
        ('Styling', 'Styling'),
    ]

    service = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    date = models.DateField()
    time = models.TimeField()
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    special_requests = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.service} on {self.date} at {self.time}"
    

# appointment

class Appointment(models.Model):
    client_name = models.CharField(max_length=255)
    service = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    staff = models.CharField(max_length=255)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"Appointment with {self.client_name} on {self.date} at {self.time}"

