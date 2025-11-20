from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from django.shortcuts import get_object_or_404
from .models import Movie, Show, Booking
from .serializers import MovieSerializer, ShowSerializer, BookingSerializer, UserRegistrationSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# --- Authentication Views ---

class SignupView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

# --- Movie & Show Views ---

class MovieListView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ShowListView(generics.ListAPIView):
    serializer_class = ShowSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Filter shows by the movie ID provided in the URL
        movie_id = self.kwargs['movie_id']
        return Show.objects.filter(movie_id=movie_id)

# --- Booking Logic ( The Core Logic) ---

class BookSeatView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={'seat_number': openapi.Schema(type=openapi.TYPE_INTEGER)},
            required=['seat_number']
        ),
        responses={201: BookingSerializer, 400: 'Bad Request'}
    )
    def post(self, request, show_id):
        seat_number = request.data.get('seat_number')
        
        if not seat_number:
            return Response({"error": "Seat number is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # PRODUCTION GRADE: Atomic Transaction
        # This ensures that all steps happen together or not at all.
        with transaction.atomic():
            # 1. Lock the show row to prevent race conditions during high traffic
            # select_for_update() locks these rows until the transaction finishes.
            show = Show.objects.select_for_update().get(id=show_id)
            
            # 2. Validate Seat Range
            if int(seat_number) < 1 or int(seat_number) > show.total_seats:
                return Response({"error": "Invalid seat number"}, status=status.HTTP_400_BAD_REQUEST)

            # 3. Check availability
            # We check if a booking exists for this seat with status 'BOOKED'
            exists = Booking.objects.filter(
                show=show, 
                seat_number=seat_number, 
                status='BOOKED'
            ).exists()

            if exists:
                return Response({"error": "Seat already booked"}, status=status.HTTP_400_BAD_REQUEST)

            # 4. Create Booking
            booking = Booking.objects.create(
                user=request.user,
                show=show,
                seat_number=seat_number,
                status='BOOKED'
            )
            
            return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)

class CancelBookingView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, booking_id):
        # Ensure user can only cancel their own bookings
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
        
        if booking.status == 'CANCELLED':
             return Response({"message": "Booking is already cancelled"}, status=status.HTTP_400_BAD_REQUEST)

        booking.status = 'CANCELLED'
        booking.save()
        return Response({"message": "Booking cancelled successfully"}, status=status.HTTP_200_OK)

class UserBookingsView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return only bookings belonging to the current user
        return Booking.objects.filter(user=self.request.user).order_by('-created_at')
