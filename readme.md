# 🎬 Movie Booking System – Backend

<div align="center">

![Django](https://img.shields.io/badge/Django-5.0+-092E20?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-3.14+-ff1709?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

A production-ready REST API for movie ticket booking with JWT authentication and concurrency-safe seat reservations.

**[Features](#-features)** • **[Installation](#%EF%B8%8F-installation)** • **[API Docs](#-api-documentation)** • **[Testing](#-testing)**

</div>

---

## ✨ Features

- 🔐 **JWT Authentication** – Secure, stateless authentication using `simplejwt`
- 🧵 **Concurrency Safe** – Prevents double-booking with database row locking
- ♻️ **Soft Deletions** – Bookings marked as `CANCELLED` for audit trails
- 📘 **Interactive Swagger UI** – Live API testing at `/swagger/`
- 🧪 **Unit Tests** – Comprehensive test coverage for edge cases
- ⚡ **Optimized Queries** – Composite indexes for fast lookups

---

## 🛠 Tech Stack

**Python 3.10+** • **Django 5.0+** • **Django REST Framework 3.14+** • **SQLite/PostgreSQL** • **drf-yasg** • **simplejwt**

---

## ⚙️ Installation

### Prerequisites
- Python 3.10+
- pip & virtualenv

### Quick Setup

```bash
# Clone repository
git clone <repository_url>
cd movie_booking_backend

# Setup environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install & migrate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser

# Run server
python manage.py runserver
```

🎉 **API running at:** `http://127.0.0.1:8000/`  
📘 **Swagger UI:** `http://127.0.0.1:8000/swagger/`

---

## 📖 API Documentation

### Main Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/signup/` | Register new user | ❌ |
| POST | `/api/login/` | Get JWT token | ❌ |
| GET | `/api/shows/` | List all shows | ✅ |
| POST | `/api/shows/{id}/book/` | Book a seat | ✅ |
| GET | `/api/bookings/` | View bookings | ✅ |
| DELETE | `/api/bookings/{id}/cancel/` | Cancel booking | ✅ |

### Authentication Flow
1. Login via `/api/login/` → get `access` token
2. In Swagger: Click **Authorize** → Enter `Bearer <token>`
3. Make authenticated requests

---

## 🧪 Testing

### Run Tests
```bash
python manage.py test bookings
```

### Quick Manual Test

**1. Register & Login**
```bash
# Register
POST /api/signup/
{"username": "john", "password": "pass123", "email": "john@example.com"}

# Login
POST /api/login/
{"username": "john", "password": "pass123"}
```

**2. Add Test Data**  
Go to `http://127.0.0.1:8000/admin/` and create:
- Movie: "Inception"
- Show: Screen 1, Today, 50 seats

**3. Book Seat**
```bash
POST /api/shows/1/book/
Authorization: Bearer <your_token>
{"seat_number": 5}
```

**Success Response:**
```json
{
  "id": 1,
  "user": "john",
  "show": 1,
  "seat_number": 5,
  "status": "CONFIRMED",
  "booking_time": "2025-01-15T10:30:00Z"
}
```

---

## 🧠 Design Decisions

### 🧵 Concurrency Control

**Challenge:** Prevent double-booking when multiple users book simultaneously.

**Solution:** Row-level locking with `transaction.atomic()` + `select_for_update()`

| Timeline | User A | User B |
|----------|--------|--------|
| T0 | Requests Seat 5 | Requests Seat 5 |
| T1 | Locks Show record | Waits for lock |
| T2 | Books seat | Still waiting |
| T3 | Commits & unlocks | Acquires lock |
| T4 | ✅ Success | ❌ Already booked |

### ⚡ Database Optimization

Composite index for fast seat checks:
```python
class Meta:
    indexes = [
        models.Index(fields=['show', 'seat_number', 'status'])
    ]
```

### ♻️ Soft Deletions

Bookings aren't deleted—status changes to `CANCELLED`:
- Maintains booking history
- Enables analytics & auditing
- Allows refund processing

---

## 📁 Project Structure

```
movie_booking_backend/
├── bookings/              # Core app
│   ├── models.py          # Movie, Show, Booking models
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # API endpoints
│   └── tests.py           # Unit tests
├── movie_booking/         # Settings
├── manage.py
└── requirements.txt
```

---

## 🚀 Production Checklist

- [ ] `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Switch to PostgreSQL
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS/SSL
- [ ] Set up CORS headers
- [ ] Add rate limiting
- [ ] Configure logging

---

## 🤝 Contributing

1. Fork the repo
2. Create feature branch (`git checkout -b feature/NewFeature`)
3. Commit changes (`git commit -m 'Add NewFeature'`)
4. Push (`git push origin feature/NewFeature`)
5. Open Pull Request

---

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

---

<div align="center">

⭐ Star if you find this helpful!

</div>
