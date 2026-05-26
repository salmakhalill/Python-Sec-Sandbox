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

🏆 **Digitopia 2025** — National ICT Competition, Ministry of Communications, Egypt  
Qualified to **Phase 3 of 4** in the Cybersecurity & AI track

</div>

---

## Overview

Most people who witness a crime don't report it — fear of being identified is the main reason. SecureReport is built around that reality: anyone can file a report anonymously, attach evidence, and track their case status without creating an account.

On the other side, the authority receiving those reports gets a full dashboard to manage cases, update statuses, and monitor trends.

This repo is the Django backend. The two React frontends were built by a teammate — my work was the API, database, analytics, and deployment, and making sure everything connected properly with the frontend.

**Live API:** `https://salmakhalill.pythonanywhere.com`

---

## What It Does

**Public portal**
- Submit a report anonymously — no registration, no identity
- Attach audio recordings, images, or documents
- Get a tracking code and follow your case through a status timeline

**Authority dashboard**
- JWT login with three roles: Admin, Employee, Viewer
- KPI cards with trend indicators — total, new, under review, critical
- Analytics charts — daily / weekly / monthly, filterable by year
- Geographic heatmap, report management, archive
- User management with welcome emails via SendGrid

**AI severity classifier** *(local only)*
- Arabic BERT model predicts severity: حرج / عالية / متوسطة / منخفضة
- Works locally but not deployed — model size doesn't fit PythonAnywhere's free tier

---

## Screenshots

### Tracking timeline — public portal
![Tracking Timeline](docs/screenshots/tracking-timeline.png)

### Analytics — authority dashboard
![Dashboard](docs/screenshots/dashboard-analytics.png)

### Welcome email
![Welcome Email](docs/screenshots/welcome-email.png)

---

## Architecture

```
┌─────────────────────┐   ┌─────────────────────┐
│  Public Portal      │   │  Authority Dashboard │
│  React              │   │  React               │
└──────────┬──────────┘   └──────────┬───────────┘
           └─────────────┬───────────┘
                         │  REST API + JWT
               ┌─────────▼──────────┐
               │   Django Backend   │
               │  accounts          │
               │  reports           │
               │  analytics         │
               └─────────┬──────────┘
                    SQLite + Media files + SendGrid
```

The backend is three apps with clear responsibilities: `accounts` handles identity and auth, `reports` is the core domain, `analytics` is a read-only layer that only aggregates data and never writes.

A few decisions worth noting — they're in [`docs/architecture.md`](docs/architecture.md) with more context:
- SQLite in production because PythonAnywhere's free tier doesn't support external DB connections
- Pandas for analytics instead of ORM aggregations — the KPI formulas came from Power BI specs and translated cleanly into DataFrame operations
- AI classifier commented out in production, not deleted — the field stays on the model and staff can set severity manually

---

## Tech Stack

| | |
|---|---|
| Framework | Django 5.2 · Django REST Framework |
| Auth | SimpleJWT — access 1h, refresh 7d |
| Database | SQLite |
| Analytics | Pandas · NumPy |
| AI | HuggingFace Transformers — Arabic BERT (local) |
| Email | SendGrid |
| Sanitization | bleach |
| Deployment | PythonAnywhere |

---

## Project Structure

```
├── config/           → settings, root URLs
├── accounts/         → users, roles, JWT, password reset, SendGrid
├── reports/          → Report, CriminalInfo, Attachment models + API
├── analytics/        → KPI computation and chart endpoints
└── media/            → uploaded files (audio, docs, images)
```

---

## API

| App | Key endpoints |
|---|---|
| reports | `POST /api/reports/` · `GET /api/reports/track/<code>/` · `PATCH /api/reports/<id>/` · `GET /api/reports/archive/` |
| analytics | `GET /analytics/recent/` · `GET /analytics/stats/` · `GET /analytics/site_stats/` |
| accounts | `POST /auth/login/` · `POST /auth/password_reset/` · `GET /account/` · `GET /users/` |

Full request/response docs: [`docs/api/`](docs/api/)

---

## Report Lifecycle

```
Submitted → Received → Under Review → In Progress → Solved  → Archive
                                                  → Closed  → Archive
```

---

## Quick Start

```bash
git clone https://github.com/salmakhalill/SecureReport_django.git
cd SecureReport_django
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate && python manage.py createsuperuser
python manage.py runserver
```

`.env` needs: `SECRET_KEY`, `DEBUG`, `SENDGRID_API_KEY`, `DEFAULT_FROM_EMAIL`

Full setup + AI classifier instructions: [`docs/setup.md`](docs/setup.md)

---

## Docs

| File | |
|---|---|
| [`docs/api/reports.md`](docs/api/reports.md) | Reports API — request/response examples |
| [`docs/api/analytics.md`](docs/api/analytics.md) | Analytics API — KPI shapes, period filter |
| [`docs/api/accounts.md`](docs/api/accounts.md) | Auth, user management, password reset |
| [`docs/database/erd.md`](docs/database/erd.md) | Entity relationship diagram |
| [`docs/database/data-dictionary.md`](docs/database/data-dictionary.md) | Field reference for all models |
| [`docs/architecture.md`](docs/architecture.md) | Technical decisions and trade-offs |
| [`docs/setup.md`](docs/setup.md) | Local setup, AI classifier, troubleshooting |

---

<div align="center">
<sub>Digitopia 2025 · Phase 3 of 4 · Egypt 🇪🇬</sub>
</div>
