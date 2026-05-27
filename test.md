# Local Setup Guide

---

## Prerequisites

- Python 3.10+
- pip
- Git

---

## 1. Clone the Repository

```bash
git clone https://github.com/salmakhalill/SecureReport_django.git
cd SecureReport_django
```

---

## 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Fill in the values:

```env
SECRET_KEY=your-django-secret-key-here
DEBUG=True
SENDGRID_API_KEY=your-sendgrid-api-key
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

**Generating a SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**SendGrid setup:**
1. Create a free account at [sendgrid.com](https://sendgrid.com)
2. Go to Settings → API Keys → Create API Key (Full Access)
3. Paste the key into `SENDGRID_API_KEY`
4. Set `DEFAULT_FROM_EMAIL` to a verified sender address

> If you don't need email in development, emails print to the console by default (`EMAIL_BACKEND = console`). No SendGrid setup needed.

---

## 5. Run Migrations

```bash
python manage.py migrate
```

---

## 6. Create a Superuser (Admin)

```bash
python manage.py createsuperuser
```

You'll be prompted for email and password. This account gets `role = Admin` automatically.

---

## 7. Start the Dev Server

```bash
python manage.py runserver
```

API available at: `http://localhost:8000`

---

## 8. Create Test Users (Optional)

Log in to the Django admin at `http://localhost:8000/admin/` with your superuser, or use the API:

```bash
# Login first to get a token
curl -X POST http://localhost:8000/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"yourpassword"}'

# Create a new Employee
curl -X POST http://localhost:8000/users/ \
  -H "Authorization: Bearer <your_access_token>" \
  -H "Content-Type: application/json" \
  -d '{"email":"employee@example.com","full_name":"Test Employee","role":"Employee"}'
```

The new user receives a welcome email with a link to set their password.

---

## 9. Run the AI Classifier Locally (Optional)

1. Download the model weights (not included in the repo — see team)
2. Point `MODEL_DIR` in `reports/ml_model.py` to the local folder
3. Uncomment the severity prediction block in `reports/views.py`:

```python
# In ReportListCreateView.perform_create():
if instance.report_details:
    from .ml_model import predict_severity
    instance.severity = predict_severity(instance.report_details)
    instance.save(update_fields=["severity"])
```

To backfill severity on existing reports:
```bash
python manage.py shell
```
```python
from reports.models import Report
from reports.ml_model import predict_severity

reports = Report.objects.filter(severity__isnull=True)
for report in reports:
    report.severity = predict_severity(report.report_details)
    report.save(update_fields=["severity"])

print(f"Updated {reports.count()} reports.")
```

---

## Project URLs Summary

| | URL |
|---|---|
| API root | `http://localhost:8000/api/` |
| Django admin | `http://localhost:8000/admin/` |
| Analytics | `http://localhost:8000/analytics/` |
| Auth | `http://localhost:8000/auth/` |
| Media files | `http://localhost:8000/media/` |

---

## Common Issues

**`SECRET_KEY` not set error**
Make sure `.env` is in the project root (same level as `manage.py`) and you've run `load_dotenv()` — it's already in `settings.py`.

**Migrations fail**
Try `python manage.py migrate --run-syncdb` or delete `db.sqlite3` and re-run migrations in a fresh dev environment.

**CORS errors from React frontend**
Add your frontend dev URL to `CORS_ALLOWED_ORIGINS` in `settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:5174",
]
```

**Emails not sending**
In development, `EMAIL_BACKEND` is set to console — check the terminal output for the email content. For real emails, set `SENDGRID_API_KEY` and switch the backend to `django.core.mail.backends.smtp.EmailBackend` (or keep using SendGrid via the API client in `email_service.py`).
