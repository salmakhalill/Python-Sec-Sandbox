# Setup

---

## Getting started

```bash
git clone https://github.com/salmakhalill/SecureReport_django.git
cd SecureReport_django

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

Create `.env` in the project root (same level as `manage.py`):

```env
SECRET_KEY=        # see below
DEBUG=True
SENDGRID_API_KEY=  # optional in dev
DEFAULT_FROM_EMAIL=
```

Generate a secret key:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Then run:
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

API at `http://localhost:8000` — Django admin at `http://localhost:8000/admin/`

---

## Email setup

In development, emails print to the terminal by default (`EMAIL_BACKEND = console`). No SendGrid needed to get started.

To send real emails: create a free account at [sendgrid.com](https://sendgrid.com), go to Settings → API Keys → Create (Full Access), then add the key and a verified sender address to `.env`. The rest is already wired up in `accounts/services/email_service.py`.

---

## Creating test users

```bash
# get a token
curl -X POST http://localhost:8000/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"yourpassword"}'

# create a staff account (welcome email sent automatically)
curl -X POST http://localhost:8000/users/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"email":"staff@example.com","full_name":"Test","role":"Employee"}'
```

Or create them directly in the Django admin at `/admin/`.

---

## AI classifier (optional)

Model weights aren't in the repo. To run locally:

1. Get the model files and point `MODEL_DIR` in `reports/ml_model.py` to that folder
2. Uncomment the prediction block in `reports/views.py`:

```python
# in ReportListCreateView.perform_create()
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

for report in Report.objects.filter(severity__isnull=True):
    report.severity = predict_severity(report.report_details)
    report.save(update_fields=["severity"])
```

---

## Troubleshooting

**`SECRET_KEY` error** — make sure `.env` is in the project root, not inside an app folder.

**Migrations fail** — delete `db.sqlite3` and re-run `migrate`, or try `--run-syncdb`.

**CORS errors from the React frontend** — add your dev URL to `CORS_ALLOWED_ORIGINS` in `settings.py`:
```python
CORS_ALLOWED_ORIGINS = ["http://localhost:5173"]
```

**Emails not arriving** — in dev they print to the terminal. Check there before debugging SendGrid.
