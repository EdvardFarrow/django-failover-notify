[![Django CI](https://github.com/EdvardFarrow/django-failover-notify/actions/workflows/ci.yml/badge.svg)](https://github.com/EdvardFarrow/django-failover-notify/actions/workflows/ci.yml)

[![ru](https://img.shields.io/badge/lang-ru-grey.svg)](README_ru.md)

# Failover Notification Service

A microservice for sending notifications with cascading delivery logic (Telegram → Email → SMS).
If the primary channel is unavailable or an error occurs, the system automatically switches to the backup.

## Features
* **Failover System:** Guaranteed message delivery, even if one of the providers is down.
* **Asynchronous:** Processing via Celery + Redis, API is not blocked.
* **Scalability:** Fully containerized (Docker Compose).
* **Clean Architecture:** Strategy pattern for channels, data validation.

## Architectural Decisions
* **Service Layer:** Sending logic has been moved from `views.py` to the service layer.
* **Strategy Pattern:** Implementing channels (Email, SMS, TG) through a common interface allows for easy addition of new communication methods (WhatsApp, Push) without changing the core code.
* **Atomic Transactions:** Using `transaction.on_commit` ensures that the task is sent to Celery only after a successful commit to the database, preventing race conditions.
* **Graceful Degradation:** The system continues to operate even if one of the external services is unavailable.

## Tech Stack
* **Python 3.12** + Django 5 + DRF
* **Celery + Redis**
* **PostgreSQL 15**
* **Docker** & Docker Compose

---

## Project Structure
```text
.
├── failover_notify/      # Project Configuration
│ ├── celery.py           # Celery and Redis Settings
│ └── settings.py         # Basic Django Settings
│
├── notifications/        # Main Application
│ ├── services/           # Business Logic
│ │ ├── channels.py       # Sending Channels
│ │ └── tasks.py          # Asynchronous Task with Retry
│ ├── admin.py            # Admin Customization
│ ├── models.py           # Models
│ ├── serializers.py      # API Validation
│ ├── tests.py            # Tests
│ └── views.py            # API controllers
│
├── docker-compose.yml    # Orchestration
├── Dockerfile            # Build instructions
├── Makefile              # Command shortcuts
├── setup.py              # Auto-deployment script
└── requirements.txt      # Dependencies
```

---

## Quick Start

I've prepared an automated installation script that will build containers, set up a database, and create test data.

### 1. Cloning
```bash
git clone <https://github.com/EdvardFarrow/django-failover-notify.git>
cd django-failover-notify
```

### 2. Automatic Installation
```bash
python setup.py
```
*Follow the on-screen instructions*

### 3. Manual Installation
```bash
# 1. Create .env (see .env.example)
# 2. Run Docker
docker compose up -d --build
# 3. Apply Migrations
docker compose exec web python manage.py migrate
```

## Testing (API)
After running the setup.py script, a test user with ID=1 will already be created in the database.
This user has no Telegram ID to demonstrate channel switching.

**Send the request:**
```bash
curl -X POST http://localhost:8000/api/send/ \
-H "Content-Type: application/json" \
-d '{
"recipient": 1,
"message": "Test message with channel switching",
"channels_chain": ["telegram", "email", "sms"]
}'
``
**Expected behavior (see logs):**

* Attempt to send to Telegram -> Error (no ID).

* Attempt to send to email -> Success (or error if the emulated failure was successful).

* Attempt to send via SMS -> Success (if email failed).

View worker logs:
```Bash
docker compose logs -f worker
```

## Monitoring and Admin Panel
The admin panel has a convenient dashboard for tracking statuses.
Sending attempt logs (channel, status, error) are displayed **Inline** — right inside the notification card.

**Access:** [http://localhost:8000/admin/](http://localhost:8000/admin/)

*(Login/password are created during installation)*

## Running tests
The project is covered with tests (API endpoints + mocks for Celery).
```bash
docker compose exec web python manage.py test
```

---

## Screenshots

### 1. Admin Panel: Notification List
Sending statuses and channels are visible (mixed email/SMS/Telegram).
![Dashboard](docs/images/admin_dashboard.png)

### 2. Detailed View: Failover Logic
Demonstration of the algorithm: Telegram attempt (error) -> Email (network error) -> SMS (success).
![Failover Logs](docs/images/admin_logs_detail.png)

### 3. Worker Logs (Terminal)
Technical confirmation of asynchronous task processing.
![Worker Logs](docs/images/terminal_logs.png)
