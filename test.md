<div align="center">

# 🛡️ SecureReport

**Anonymous crime reporting platform with authority dashboard**

![Django](https://img.shields.io/badge/Django-5.2-092E20?style=flat-square&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-3.x-ff1709?style=flat-square&logo=django&logoColor=white)
![JWT](https://img.shields.io/badge/Auth-JWT-black?style=flat-square&logo=jsonwebtokens&logoColor=white)
![React](https://img.shields.io/badge/Frontend-React-61DAFB?style=flat-square&logo=react&logoColor=black)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white)
![SendGrid](https://img.shields.io/badge/Email-SendGrid-1A82E2?style=flat-square&logo=sendgrid&logoColor=white)
![PythonAnywhere](https://img.shields.io/badge/Deploy-PythonAnywhere-1D9FD7?style=flat-square)

<br/>

> 🏆 **Digitopia 2025** — National ICT Competition, Ministry of Communications, Egypt
> Qualified to **Phase 3 out of 4** competing in the Cybersecurity & AI track

<br/>

**This repository is the backend.**
Frontend (React) was built by a teammate — I owned the API design, integration, and deployment.

**Live API:** `https://salmakhalill.pythonanywhere.com`

</div>

---

## The Problem

Most people who witness or experience a crime never report it. The main reason isn't indifference — it's fear of being identified.

SecureReport removes that barrier entirely. Submit a report anonymously, attach evidence, and track your case through a live status timeline. No account. No identity.

---

## What's in This Repo

Two React apps, one Django backend:

**Public portal** — anonymous report submission, file uploads, and a tracking code that shows the reporter exactly where their case stands via a visual timeline.

**Authority dashboard** — the receiving organization logs in, reviews incoming reports, updates case status, monitors KPIs, and exports trends from an analytics module.

---

## Screenshots

### Public portal — track your report
![Tracking Timeline](docs/screenshots/tracking-timeline.png)

### Authority dashboard — analytics
![Dashboard](docs/screenshots/dashboard-analytics.png)

### System emails
![Welcome Email](docs/screenshots/welcome-email.png)

---

## Features

**Public portal**
- Anonymous submission — zero registration required
- 5 report types: Assault, Blackmail, Harassment, Theft, Altercation
- Location field with map link and GPS coordinates
- Attach audio recordings, images, or documents
- Auto-generated 12-character tracking code per report
- Visual status timeline on the tracking page

**Authority dashboard**
- JWT-secured login with role-based access (Admin / Employee / Viewer)
- KPI cards with trend comparison: total, new, under review, critical reports
- Analytics charts filterable by year and period (daily / weekly / monthly)
- Geographic heatmap of incidents
- Reports table — update status, move cases to archive on resolution
- User management (Admin only) — create users, assign roles, send welcome emails
- Password reset via email (SendGrid)

**AI severity classifier** *(local only)*
- Arabic BERT model, fine-tuned to predict severity: حرج / عالية / متوسطة / منخفضة
- Runs at submission time on `report_details` text
- Not deployed — model size exceeds PythonAnywhere limits

---

## Architecture

```
┌──────────────────────┐   ┌──────────────────────┐
│   Public Portal      │   │  Authority Dashboard  │
│   React              │   │  React                │
└────────┬─────────────┘   └──────────┬────────────┘
         │                            │
         └──────────────┬─────────────┘
                        │  REST API · CORS · JWT
              ┌─────────▼──────────────┐
              │     Django Backend     │
              │                        │
              │  reports/              │
              │  accounts/             │
              │  analytics/            │
              └───┬────────────────────┘
                  │
        ┌─────────┴──────────┐
        │      SQLite        │   + Media files (audio, docs)
        └────────────────────┘   + SendGrid (email)
```

---

## Tech Stack

| | |
|---|---|
| Framework | Django 5.2 · Django REST Framework |
| Auth | SimpleJWT — access 1h · refresh 7d |
| Database | SQLite |
| Analytics | Pandas · NumPy — translated from Power BI specs |
| AI Model | HuggingFace Transformers — BERT fine-tuned on Arabic |
| Email | SendGrid |
| Input sanitization | bleach |
| Security | Secure cookies · HTTPS redirect · XSS/clickjacking protection |
| Deployment | PythonAnywhere |

---

## Project Structure

```
├── config/           → Django settings · root URLs
├── accounts/         → Custom user model · JWT · roles · password reset
│   ├── services/
│   │   ├── auth_service.py    → uid/token helpers
│   │   └── email_service.py   → SendGrid integration
│   └── templates/accounts/emails/
├── reports/          → Core report logic
│   ├── models.py     → Report · CriminalInfo · Attachment
│   ├── serializers.py → Nested serializers · input sanitization
│   ├── views.py      → List · Create · Update · Delete · Track · Archive
│   └── ml_model.py   → BERT classifier (local only)
└── analytics/        → Dashboard data
    ├── utils.py      → Pandas/NumPy processing · KPI helpers
    └── views.py      → REST endpoints
```

---

## API Reference

### Reports

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/api/reports/` | Public | Submit anonymous report |
| `GET` | `/api/reports/` | Required | List active reports |
| `GET` | `/api/reports/track/<code>/` | Public | Track report by code |
| `GET` | `/api/reports/archive/` | Required | Solved / closed reports |
| `PATCH` | `/api/reports/<id>/` | Admin · Employee | Update report |
| `DELETE` | `/api/reports/<id>/` | Admin · Employee | Delete report |

### Analytics

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/analytics/stats/` | Required | KPIs and charts — filterable by year |
| `GET` | `/analytics/recent/` | Required | Recent KPIs — daily / weekly / monthly |
| `GET` | `/analytics/site_stats/` | Public | Stats for public landing page |

### Accounts

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/auth/login/` | Public | Login — returns JWT + role |
| `POST` | `/auth/refresh/` | Public | Refresh access token |
| `POST` | `/auth/password_reset/` | Public | Send reset email |
| `POST` | `/auth/password_reset_confirm/<uid>/<token>/` | Public | Confirm new password |
| `GET · PATCH` | `/account/` | Active user | View or update own account |
| `GET · POST · PATCH · DELETE` | `/users/` | Admin only | Manage all users |

---

## User Roles

| | View reports | Update status | Delete | Manage users |
|---|---|---|---|---|
| Admin | Full detail | Yes | Yes | Yes |
| Employee | Full detail | Yes | Yes | No |
| Viewer | Limited fields | No | No | No |

Inactive users receive empty responses regardless of role.

---

## Report Lifecycle

```
Submitted → Received → Under Review → In Progress ┬→ Solved ──→ Archive
                                                   └→ Closed ──→ Archive
```

---

## Local Setup

```bash
git clone https://github.com/salmakhalill/SecureReport_django.git
cd SecureReport_django

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env          # fill in the values below

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

**Required environment variables:**

```env
SECRET_KEY=
DEBUG=True
SENDGRID_API_KEY=
DEFAULT_FROM_EMAIL=
```

---

## AI Severity Classifier

Fine-tuned BERT for Arabic crime report text. Labels: حرج / عالية / متوسطة / منخفضة

To run locally — set `MODEL_DIR` in `reports/ml_model.py`, then uncomment the call in `views.py`.

Backfill existing reports:

```python
# python manage.py shell
from reports.models import Report
from reports.ml_model import predict_severity

for report in Report.objects.filter(severity__isnull=True):
    report.severity = predict_severity(report.report_details)
    report.save(update_fields=["severity"])
```

---

## Docs

- [`docs/database/erd.png`](docs/database/erd.png) — entity relationship diagram
- [`docs/database/data-dictionary.md`](docs/database/data-dictionary.md) — field reference
- [`docs/sequence-diagrams.md`](docs/sequence-diagrams.md) — auth, submission, password reset flows
- [`docs/class-diagram.md`](docs/class-diagram.md) — model relationships

---

<div align="center">
<sub>Digitopia 2025 · Phase 3 of 4 · Built for a safer Egypt 🇪🇬</sub>
</div>
