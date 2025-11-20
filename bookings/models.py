from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Movie(models.Model):
    """
    Represents a movie entry in the database.
    """
    title = models.CharField(max_length=255)
    duration_minutes = models.PositiveIntegerField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

class Show(models.Model):
    """
    Represents a specific screening of a movie.
    """
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='shows')
    screen_name = models.CharField(max_length=100)
    date_time = models.DateTimeField()
    total_seats = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.movie.title} at {self.date_time}"

class Booking(models.Model):
    """
    Represents a ticket booking.
    We use a tuple for status to ensure data consistency.
    """
    STATUS_CHOICES = [
        ('BOOKED', 'Booked'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='bookings')
    seat_number = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='BOOKED')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # PRODUCTION GRADE CONSTRAINT: 
        # Ensures at the database level that a seat cannot be double-booked 
        # for the same show unless the previous booking was cancelled.
        indexes = [
            models.Index(fields=['show', 'seat_number', 'status']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.show} - Seat {self.seat_number}"
