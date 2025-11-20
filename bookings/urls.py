from django.urls import path
from .views import (
    SignupView, MovieListView, ShowListView, 
    BookSeatView, CancelBookingView, UserBookingsView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Auth
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # Movies & Shows
    path('movies/', MovieListView.as_view(), name='movie-list'),
    path('movies/<int:movie_id>/shows/', ShowListView.as_view(), name='show-list'),
    
    # Booking Actions
    path('shows/<int:show_id>/book/', BookSeatView.as_view(), name='book-seat'),
    path('bookings/<int:booking_id>/cancel/', CancelBookingView.as_view(), name='cancel-booking'),
    path('my-bookings/', UserBookingsView.as_view(), name='my-bookings'),
]
