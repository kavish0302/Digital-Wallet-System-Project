# Digital Wallet System

A Django-based digital wallet with multi-currency cash management, validation, and fraud detection.  
Provides a web UI, REST API with Swagger documentation, scheduled tasks, and containerized setup.

---

## 🔑 Default Accounts

Use these credentials to log in immediately:

| Role       | Username | Password    |
|------------|----------|-------------|
| **Admin**  | Kavish   | gulati@8989 |
| **Tester** | tester   | test@1234   |

---

## 🛠️ Technology Stack

- **Backend**: Python 3.12, Django 5.2.1  
- **Async & Scheduling**: Celery 5 + Redis  
- **API**: Django REST Framework + drf-yasg (Swagger UI)  
- **Database**: SQLite (development) / PostgreSQL (production)  
- **Containerization**: Docker & Docker Compose  
- **CI**: GitHub Actions  
- **Frontend**: Django Templates + Bootstrap 5  

---

## 📋 Key Features

1. **User Authentication**  
   - Register, Log in, Log out  
   - “Show password” toggle & “Forgot password” reset flow  
2. **Wallet Operations**  
   - Deposit, Withdraw, Transfer funds  
   - Support for multiple currencies (INR, USD, etc.)  
   - Transaction history per user  
3. **Validation & Atomicity**  
   - Overdraft protection, minimum amount checks  
   - All operations wrapped in atomic transactions  
4. **Fraud Detection**  
   - Flags for rapid transfers & large withdrawals  
   - Immediate email alerts (console backend in dev)  
   - Daily Celery-beat scans with summary email  
5. **Soft Delete**  
   - `is_active` flag on Wallet & Transaction for data retention  
6. **Reporting & Admin API**  
   - Admin web view for flagged transactions  
   - REST endpoints for flags, balances, top users  
   - Swagger UI available at `/swagger/`  

---

## 🚀 Quick Start (Local)

### Prerequisites

- Python 3.8+ and pip  
- Redis server  
- (Optional) Docker & Docker Compose

### 1. Clone or Download

Download the repository ZIP or clone via your preferred Git client into a directory containing `manage.py`.

### 2. Python Environment

```bash
cd <project-root>
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Database Setup

```bash
python manage.py migrate
```

### 4. Seed Default Currencies

```bash
python manage.py shell
>>> from wallet_app.models import Currency
>>> Currency.objects.create(id=1, code='INR', name='Indian Rupee')
>>> Currency.objects.create(code='USD', name='US Dollar')
>>> exit()
```

### 5. (Optional) Create Superuser

```bash
python manage.py createsuperuser
# or use default Admin credentials above
```

### 6. Start Services

In one terminal:

```bash
redis-server &
python manage.py runserver
```

In another terminal:

```bash
celery -A wallet_project worker --beat --loglevel=info
```

### 7. Browse the App

- **Main UI**: http://127.0.0.1:8000/  
- **Admin Panel**: http://127.0.0.1:8000/admin/  
- **Swagger UI**: http://127.0.0.1:8000/swagger/  

Log in as **Kavish / gulati@8989** (Admin) or **tester / test@1234** (Tester).

---

## 🐳 Docker Compose

```bash
docker-compose up --build
```

- **web**: Django + Celery + Redis  
- **redis**: Redis service  
- Ports: 8000 → Django, 6379 → Redis

---

## 🧪 Running Tests

```bash
python manage.py test
```

---

## 📘 API Testing

- **Swagger UI** at `/swagger/` is the primary API explorer.  
- (Optional) Use `curl`:
  ```bash
  curl -u Kavish:gulati@8989 http://127.0.0.1:8000/api/flags/
  ```

---

## 📤 Submission & CI

- A `.github/workflows/ci.yml` is included for GitHub Actions CI.  
- Tests, migrations, and linting run on each push/pull request.  

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
