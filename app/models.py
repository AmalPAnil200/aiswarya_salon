from django.db import models

    
class Booking(models.Model):
    SERVICE_CHOICES = [
        ('Haircut', 'Haircut'),
        ('Hair Color', 'Hair Color'),
        ('Beard Dressing', 'Beard Dressing'),
        ('Shaving', 'Shaving'),
    ]

    # Add a ForeignKey to Customer
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
    

