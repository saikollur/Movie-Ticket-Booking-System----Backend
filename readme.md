# 🎬 Movie Booking System – Backend

<div align="center">

![Django](https://img.shields.io/badge/Django-5.0+-092E20?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-3.14+-ff1709?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

A production-ready REST API for a movie ticket booking system, built with Django and Django REST Framework.

**Secure • Concurrent • Interactive**

[Features](#-features) • [Installation](#%EF%B8%8F-installation--setup) • [API Docs](#-api-documentation) • [Testing](#-testing)

</div>

---

## ✨ Features

- 🔐 **JWT Authentication** – Secure, stateless authentication using `simplejwt`
- 🧵 **Concurrency Safe** – Prevents double-booking with database row locking
- ♻️ **Soft Deletions** – Bookings are marked as `CANCELLED` instead of deleted
- 📘 **Interactive API Docs** – Swagger UI with live testing capabilities
- 🧪 **Comprehensive Tests** – Unit tests for booking logic, concurrency, and edge cases
- 🚀 **Production Ready** – Optimized queries with composite indexes

---

## 🛠 Tech Stack

| Technology                        | Purpose                                              |
| --------------------------------- | ---------------------------------------------------- |
| **Python 3.10+**                  | Core language                                        |
| **Django 5.0+**                   | Web framework                                        |
| **Django REST Framework 3.14+**   | RESTful API development                              |
| **SQLite / PostgreSQL**           | Database (SQLite for dev, PostgreSQL for production) |
| **drf-yasg**                      | Swagger/OpenAPI documentation                        |
| **djangorestframework-simplejwt** | JWT authentication                                   |

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone <repository_url>
cd movie_booking_backend
```

### 2️⃣ Create & Activate Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Database Setup

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### 5️⃣ Create Admin User

```bash
python manage.py createsuperuser
```

Follow the prompts to set your admin credentials.

### 6️⃣ Run Development Server

```bash
python manage.py runserver
```

🎉 **Your API is now live at:** `http://127.0.0.1:8000/`

---

## 📖 API Documentation

### 🌐 Access Swagger UI

Visit: **[http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)**

### 🔓 Authorization Setup

1. Login using `/api/login/` endpoint
2. Copy the `access` token from response
3. Click **Authorize** button in Swagger UI
4. Enter: `Bearer <your_access_token>`
5. Click **Authorize** to confirm

---

## 🧪 Testing

### Run Unit Tests

```bash
python manage.py test bookings
```

### Manual Testing Flow

#### 1️⃣ **Register a New User**

```http
POST /api/signup/
Content-Type: application/json

{
  "username": "john",
  "password": "securepass123",
  "email": "john@example.com"
}
```

#### 2️⃣ **Login**

```http
POST /api/login/
Content-Type: application/json

{
  "username": "john",
  "password": "securepass123"
}
```

**Response:**

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### 3️⃣ **Add Test Data (Admin Only)**

Visit Django Admin: **[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)**

Add:

- **Movie** (e.g., "Inception")
- **Show** (e.g., Screen 1, Today, 50 seats)

#### 4️⃣ **Book a Seat**

```http
POST /api/shows/1/book/
Authorization: Bearer <your_access_token>
Content-Type: application/json

{
  "seat_number": 5
}
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

### 🧵 Concurrency & Double Booking Prevention

**Problem:** Multiple users booking the same seat simultaneously.

**Solution:**

- Wrapped booking logic in `transaction.atomic()`
- Used `select_for_update()` for row-level locking
- Prevents race conditions at database level

**Example Scenario:**

| Timeline | User A                  | User B                |
| -------- | ----------------------- | --------------------- |
| T0       | Requests Seat 5         | Requests Seat 5       |
| T1       | Locks Show row          | Waits for lock        |
| T2       | Books seat              | Still waiting         |
| T3       | Commits & releases lock | Gets lock             |
| T4       | ✅ Success              | ❌ Seat already taken |

### ⚡ Database Optimization

Added composite index on `Booking` model:

```python
class Meta:
    indexes = [
        models.Index(fields=['show', 'seat_number', 'status'])
    ]
```

**Benefits:**

- Lightning-fast seat availability checks
- Optimized filtering by show and status
- Improved query performance for large datasets

### ♻️ Soft Deletions

Bookings are never permanently deleted:

- Cancelled bookings are marked as `status='CANCELLED'`
- Enables audit trails and analytics
- Allows potential restoration if needed

---

## 📁 Project Structure

```
movie_booking_backend/
│
├── bookings/              # Main app
│   ├── models.py          # Database models
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # API views
│   ├── urls.py            # URL routing
│   └── tests.py           # Unit tests
│
├── movie_booking/         # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🔒 Security Features

- ✅ JWT-based authentication
- ✅ Password hashing with Django's default PBKDF2
- ✅ CSRF protection enabled
- ✅ SQL injection prevention via ORM
- ✅ Rate limiting (recommended for production)

---

## 🚀 Deployment Checklist

Before deploying to production:

- [ ] Set `DEBUG = False` in settings
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Switch to PostgreSQL database
- [ ] Set strong `SECRET_KEY`
- [ ] Configure CORS headers
- [ ] Add rate limiting (django-ratelimit)
- [ ] Set up logging and monitoring
- [ ] Use environment variables for secrets
- [ ] Configure HTTPS/SSL
- [ ] Set up database backups

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📧 Contact

Have questions or suggestions? Feel free to open an issue or reach out!

---

<div align="center">

**Made with ❤️ using Django**

⭐ Star this repo if you find it helpful!

</div>
