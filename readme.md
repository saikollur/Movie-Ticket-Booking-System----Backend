🎬 Movie Booking System – Backend

A production-ready REST API for a movie ticket booking system, built using Django and Django REST Framework (DRF).
This backend features secure JWT authentication, concurrency-safe seat booking, and interactive Swagger documentation.

🚀 Features

🔐 JWT Authentication with simplejwt for secure, stateless login.

🧵 Concurrency Handling using:

transaction.atomic()

select_for_update() row locking
Prevents double-booking of seats.

♻️ Soft Cancellations
Bookings are marked as CANCELLED instead of being deleted.

📘 Swagger / OpenAPI Docs
Available at: /swagger/

🧪 Unit Tests
Tests written for booking rules, concurrency, and edge cases.

🛠 Tech Stack

🐍 Python 3.10+

🏗 Django 5.0+

🔧 Django REST Framework 3.14+

🗄 SQLite (Dev) / PostgreSQL (Production-ready)

📄 drf-yasg for API documentation

⚙️ Installation & Setup
1. Clone the Repository
git clone <repository_url>
cd movie_booking_backend

2. Create Virtual Environment
python -m venv venv


Activate Environment

Windows:

venv\Scripts\activate


macOS/Linux:

source venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

🗄 Database Setup

Apply migrations:

python manage.py makemigrations
python manage.py migrate

🔑 Create Admin User
python manage.py createsuperuser


Follow the prompts to set username & password.

▶️ Run the Development Server
python manage.py runserver


Your API is now live at:
👉 http://127.0.0.1:8000/

🧪 Run Unit Tests
python manage.py test bookings

📖 API Documentation

🚪 Visit Swagger UI:
👉 http://127.0.0.1:8000/swagger/

Authorize

Login using /api/login/

Copy the access token

Click Authorize in Swagger

Enter:

Bearer <your_access_token>

🧪 Manual Testing Guide
1. Register

POST /api/signup/

{
  "username": "john",
  "password": "securepass123",
  "email": "john@example.com"
}

2. Login

POST /api/login/

{
  "username": "john",
  "password": "securepass123"
}


Copy the access token from the response.

3. Add Data (Admin Only)

Visit Django admin:
👉 http://127.0.0.1:8000/admin/

Add:

Movie (example: Inception)

Show (example: Screen 1, Today, 50 seats)

4. Book a Seat

POST /api/shows/1/book/

Header:

Authorization: Bearer <your_token>


Body:

{
  "seat_number": 5
}

🧠 Design Decisions
🧵 Concurrency & Double Booking Prevention

To handle simultaneous bookings:

Wrapped booking process inside transaction.atomic()

Used select_for_update() to lock the Show row

Example Scenario
User A and User B try to book Seat 5 at the exact same moment.

Outcome:
User A’s request locks the seat first.
User B’s request waits → detects seat already booked → fails gracefully.

⚡ Database Optimization

A composite index was added on the Booking model:

['show', 'seat_number', 'status']


This makes seat availability checks extremely fast.

🤝 Contributing

Pull requests and bug reports are welcome!
