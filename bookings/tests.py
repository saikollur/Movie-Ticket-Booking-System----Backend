from django.test import TestCase
from django.contrib.auth.models import User
from .models import Movie, Show, Booking
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status

class BookingLogicTests(TestCase):
    def setUp(self):
        # 1. Setup Data
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.user2 = User.objects.create_user(username='otheruser', password='password123')
        
        self.movie = Movie.objects.create(title="Inception", duration_minutes=148)
        self.show = Show.objects.create(
            movie=self.movie,
            screen_name="Screen 1",
            date_time=timezone.now(),
            total_seats=50
        )
        
        # 2. Setup API Client
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_book_seat_success(self):
        """Test that a valid seat can be booked."""
        response = self.client.post(f'/api/shows/{self.show.id}/book/', {'seat_number': 1})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Booking.objects.filter(seat_number=1, status='BOOKED').exists())

    def test_prevent_double_booking(self):
        """Test that the same seat cannot be booked twice."""
        # First booking
        self.client.post(f'/api/shows/{self.show.id}/book/', {'seat_number': 5})
        
        # Second booking attempt (same user or different user)
        response = self.client.post(f'/api/shows/{self.show.id}/book/', {'seat_number': 5})
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Booking.objects.filter(seat_number=5, status='BOOKED').count(), 1)

    def test_cancel_booking(self):
        """Test that a booking can be cancelled and the seat freed up."""
        # 1. Book
        booking = Booking.objects.create(user=self.user, show=self.show, seat_number=10, status='BOOKED')
        
        # 2. Cancel
        response = self.client.post(f'/api/bookings/{booking.id}/cancel/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        booking.refresh_from_db()
        self.assertEqual(booking.status, 'CANCELLED')

        # 3. Try to book the seat again (should succeed now)
        response = self.client.post(f'/api/shows/{self.show.id}/book/', {'seat_number': 10})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_prevent_booking_invalid_seat(self):
        """Test that you cannot book a seat outside the total_seats range."""
        response = self.client.post(f'/api/shows/{self.show.id}/book/', {'seat_number': 999})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
