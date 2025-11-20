Movie Booking System Backend

A robust, production-ready REST API for a movie ticket booking system, built with Django and Django REST Framework. This project features JWT authentication, atomic transactions for data integrity, and automated Swagger documentation.

🚀 Features

JWT Authentication: Secure, stateless authentication using simplejwt.

Concurrency Handling: Uses transaction.atomic and database row locking (select_for_update) to prevent double-booking of seats.

Soft Cancellations: Bookings are marked as 'CANCELLED' rather than deleted, preserving data history.

Swagger/OpenAPI Documentation: Interactive API explorer available at /swagger/.

Unit Tests: Comprehensive testing for booking rules and edge cases.

🛠 Tech Stack

Python (3.10+)

Django (5.0+)

Django REST Framework (3.14+)

Database: SQLite (Dev) / PostgreSQL (Production ready)

Documentation: drf-yasg (Swagger UI)

⚙️ Setup Instructions

Follow these steps to set up the project locally.

1. Clone and Install

# Clone the repository

git clone <repository_url>
cd movie_booking_backend

# Create a virtual environment

python -m venv venv

# Activate the virtual environment

# On Windows:

venv\Scripts\activate

# On macOS/Linux:

source venv/bin/activate

# Install dependencies

pip install -r requirements.txt

2. Database Setup

Apply the database migrations to create the necessary tables.

python manage.py makemigrations
python manage.py migrate

3. Create an Admin User

You need a superuser to access the Django Admin panel and add Movies/Shows.

python manage.py createsuperuser

Follow the prompts to set a username and password.

4. Run the Server

python manage.py runserver

The server will start at http://127.0.0.1:8000/.

5. Run Tests (Bonus)

To verify the booking logic and concurrency rules:

python manage.py test bookings

📖 API Documentation & Usage

The easiest way to test the API is using the integrated Swagger UI.

Open the Docs: Navigate to http://127.0.0.1:8000/swagger/.

Authorize:

Use the /api/login/ endpoint to get an access token.

Click the Authorize button at the top of the Swagger page.

Enter: Bearer <your_access_token> (Note the space after "Bearer").

🧪 Testing Workflow (Manual)

Register:

POST /api/signup/

Body: {"username": "john", "password": "securepass123", "email": "john@example.com"}

Login:

POST /api/login/

Body: {"username": "john", "password": "securepass123"}

Response: Copy the access token.

Add Data (Admin Only):

Go to http://127.0.0.1:8000/admin/

Create a Movie (e.g., "Inception").

Create a Show (e.g., Inception, Screen 1, Today, 50 Seats). Note the id of the show (e.g., 1).

Book a Seat:

POST /api/shows/1/book/

Header: Authorization: Bearer <your_token>

Body: {"seat_number": 5}

🧠 Design Decisions

Concurrency & Double Booking

To satisfy the requirement of preventing double bookings, I implemented pessimistic locking using select_for_update() within an atomic transaction.

Scenario: User A and User B try to book Seat 5 at the exact same millisecond.

Solution: The database locks the Show row when User A starts the booking process. User B's request waits until User A's transaction commits or rolls back. If User A succeeds, User B's check will fail gracefully with "Seat already booked".

Database Indexes

An index was added to the Booking model on ['show', 'seat_number', 'status'] to optimize lookups when checking seat availability.
