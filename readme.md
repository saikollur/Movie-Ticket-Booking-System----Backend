# 🎬 Movie Booking System – Backend

<div align="center">

![Django](https://img.shields.io/badge/Django-5.0+-092E20?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-3.14+-ff1709?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)

A production-ready REST API for movie ticket booking with JWT authentication and concurrency-safe seat reservations.

</div>

---

## ✨ Features

- 🔐 **JWT Authentication** – Secure token-based auth
- 🧵 **Concurrency Safe** – Prevents double-booking with row locking
- ♻️ **Soft Deletions** – Bookings marked as cancelled, not deleted
- 📘 **Swagger Docs** – Interactive API documentation at `/swagger/`
- 🧪 **Unit Tests** – Comprehensive test coverage

## 🛠 Tech Stack

**Python 3.10+** • **Django 5.0+** • **Django REST Framework** • **SQLite/PostgreSQL** • **drf-yasg** • **simplejwt**

---

## ⚙️ Quick Start

```bash
# Clone and setup
git clone <repository_url>
cd movie_booking_backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Database setup
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# Run server
python manage.py runserver
```

🎉 **API live at:** `http://127.0.0.1:8000/`  
📖 **Swagger UI:** `http://127.0.0.1:8000/swagger/`

---

## 🧪 Quick Test

```bash
# 1. Register
POST /api/signup/
{"username": "john", "password": "pass123", "email": "john@example.com"}

# 2. Login (get token)
POST /api/login/
{"username": "john", "password": "pass123"}

# 3. Book seat
POST /api/shows/1/book/
Headers: Authorization: Bearer <token>
Body: {"seat_number": 5}
```

**Run Tests:**

```bash
python manage.py test bookings
```

---

## 🧠 Key Design Decisions

**Concurrency Control:**  
Uses `transaction.atomic()` + `select_for_update()` to prevent race conditions. When two users book the same seat simultaneously, one succeeds while the other receives an error.

**Database Optimization:**  
Composite index on `['show', 'seat_number', 'status']` for fast seat availability checks.

**Soft Deletions:**  
Cancelled bookings retain status history for auditing and analytics.

---

## 🤝 Contributing

Contributions welcome! Fork, create a feature branch, and submit a PR.

---

<div align="center">

• ⭐ Star if helpful!

</div>
