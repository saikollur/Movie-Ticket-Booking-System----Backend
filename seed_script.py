from django.contrib.auth.models import User
from bookings.models import Movie, Show, Booking
from django.utils import timezone
from datetime import timedelta
import random

# --- Configuration ---
NUM_MOVIES = 5
SEATS_PER_SHOW = 100
SHOWS_PER_MOVIE = 3
INITIAL_BOOKINGS = 10

# Helper function for generating unique movie titles
MOVIE_TITLES = [
    "Interstellar Journey", "The Silent Witness", "Code Red", 
    "Echoes of Yesterday", "The Last Stand", "Midnight Train"
]

def generate_seed_data():
    """
    Deletes all existing Movies, Shows, and Bookings, and recreates fresh data.
    """
    print("--- Starting Database Seeder ---")
    
    # 1. Clear existing data
    Booking.objects.all().delete()
    Show.objects.all().delete()
    Movie.objects.all().delete()
    User.objects.filter(username__startswith='seed_user').delete()
    
    print("Cleaned existing data (Bookings, Shows, Movies, Seed Users).")

    # 2. Create sample user (for bookings)
    try:
        if not User.objects.filter(username='seed_user').exists():
            user = User.objects.create_user('seed_user', 'seed@example.com', 'seedpass')
            print(f"Created sample user: {user.username}")
        else:
            user = User.objects.get(username='seed_user')
            
    except Exception as e:
        print(f"Error creating seed user: {e}")
        return

    # 3. Create Movies
    movies = []
    for i in range(NUM_MOVIES):
        title = MOVIE_TITLES[i % len(MOVIE_TITLES)] + f" ({i+1})"
        movie = Movie.objects.create(
            title=title,
            duration_minutes=random.randint(90, 150),
            description=f"A compelling synopsis for the movie {title}."
        )
        movies.append(movie)
        print(f"Created Movie: {movie.title}")

    # 4. Create Shows for each Movie
    shows = []
    for movie in movies:
        for j in range(SHOWS_PER_MOVIE):
            # Show times: one today, one tomorrow, one day after
            show_time = timezone.now() + timedelta(days=j, hours=random.randint(18, 22), minutes=random.randrange(0, 60, 15))
            
            show = Show.objects.create(
                movie=movie,
                screen_name=f"Screen {j+1}",
                date_time=show_time,
                total_seats=SEATS_PER_SHOW
            )
            shows.append(show)
            print(f" - Created Show: {show}")

    # 5. Create initial Bookings
    booked_count = 0
    for show in random.sample(shows, min(len(shows), 5)): # Book seats in 5 random shows
        booked_seats = set()
        for _ in range(INITIAL_BOOKINGS):
            seat_number = random.randint(1, SEATS_PER_SHOW)
            
            # Ensure unique seat in this loop instance
            while seat_number in booked_seats:
                seat_number = random.randint(1, SEATS_PER_SHOW)

            Booking.objects.create(
                user=user,
                show=show,
                seat_number=seat_number,
                status='BOOKED'
            )
            booked_seats.add(seat_number)
            booked_count += 1
            
    print(f"Created {len(movies)} Movies, {len(shows)} Shows, and {booked_count} Bookings.")
    print("--- Seeding Complete ---")

if __name__ == '__main__':
    # This setup is necessary to run the script outside of the Django shell
    import django
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    
    generate_seed_data()
