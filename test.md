<div align="center">

# 🛡️ SecureReport

**Anonymous crime reporting platform with authority dashboard**

<br/>

![Django](https://img.shields.io/badge/Django-5.2-092E20?style=flat-square&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-3.x-ff1709?style=flat-square&logo=django&logoColor=white)
![JWT](https://img.shields.io/badge/Auth-JWT-black?style=flat-square&logo=jsonwebtokens&logoColor=white)
![React](https://img.shields.io/badge/Frontend-React-61DAFB?style=flat-square&logo=react&logoColor=black)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white)
![SendGrid](https://img.shields.io/badge/Email-SendGrid-1A82E2?style=flat-square&logo=sendgrid&logoColor=white)
![PythonAnywhere](https://img.shields.io/badge/Deploy-PythonAnywhere-1D9FD7?style=flat-square)

<br/>

🏆 **Digitopia 2025** — National ICT Competition under Egypt's Ministry of Communications  
Reached **Phase 3 of 4** in the Cybersecurity & AI track

<br/>

**Live API →** `https://salmakhalill.pythonanywhere.com`

</div>

---

## About

Most people who witness a crime don't report it — fear of being identified is the main reason.

SecureReport lets anyone file a report completely anonymously, attach evidence, and track their case through a status timeline. No account needed. On the other side, the authority receiving reports gets a full dashboard to manage cases, update statuses, and monitor trends.

> **This repo is the Django backend.**
> The two React frontends were built by a teammate. My role was the API, database design, analytics module, and deployment — plus the integration work to connect everything with the frontend.

---

## Screenshots

| Public portal — status timeline | Authority dashboard |
|---|---|
| ![Tracking](docs/screenshots/tracking-timeline.png) | ![Dashboard](docs/screenshots/dashboard-analytics.png) |

<div align="center">

![Welcome Email](docs/screenshots/welcome-email.png)  
*Welcome email sent via SendGrid when a new staff account is created*

</div>

---

## Features

<details>
<summary><b>Public Portal</b></summary>

<br/>

- Anonymous submission — no registration, no identity required
- 5 report types: Assault · Blackmail · Harassment · Theft · Altercation
- Location with map link and GPS coordinates
- Attach audio recordings, images, or documents
- Auto-generated 12-character tracking code per report
- Visual status timeline — see exactly where the case stands

</details>

<details>
<summary><b>Authority Dashboard</b></summary>

<br/>

- JWT-secured login with role-based access — Admin, Employee, Viewer
- KPI cards with trend indicators: total, new, under review, critical reports
- Analytics charts filterable by year — daily / weekly / monthly toggle
- Geographic heatmap of incidents
- Reports table — update status, manage active cases
- Archive — cases auto-move here when solved or closed
- User management: create accounts, assign roles, send welcome emails
- Password reset via SendGrid

</details>

<details>
<summary><b>AI Severity Classifier</b> <i>(local only)</i></summary>

<br/>

Fine-tuned Arabic BERT model that predicts report severity at submission time:  
**حرج / عالية / متوسطة / منخفضة**

Not deployed — model size exceeds PythonAnywhere limits. The `severity` field stays on the model and can be set manually by staff, or populated via the backfill script in `reports/ml_model.py`.

</details>

---

## Architecture

```
┌─────────────────────┐     ┌──────────────────────┐
│   Public Portal     │     │  Authority Dashboard  │
│   React             │     │  React                │
└──────────┬──────────┘     └──────────┬────────────┘
           └──────────────┬────────────┘
                          │  REST API · CORS · JWT
                ┌─────────▼───────────┐
                │    Django Backend   │
                │                     │
                │  accounts/          │
                │  reports/           │
                │  analytics/         │
                └─────────┬───────────┘
                          │
              ┌───────────┴────────────┐
              │        SQLite          │
              └────────────────────────┘
              Media files · SendGrid
```

**A few decisions worth knowing about** — full context in [`docs/architecture.md`](docs/architecture.md):

- **SQLite in production** — PythonAnywhere's free tier doesn't support external DB connections. Settings include the PostgreSQL config commented out for when that changes.
- **Pandas for analytics** — the KPI formulas came from Power BI specs provided by the data analyst teammate and translated naturally into DataFrame operations.
- **AI classifier is commented out, not removed** — the field stays on the model, staff can set severity manually in the meantime.

---

## Tech Stack

| | |
|---|---|
| Framework | Django 5.2 + Django REST Framework |
| Auth | SimpleJWT — access 1h · refresh 7d |
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
├── accounts/         → users, roles, JWT auth, password reset, SendGrid
├── reports/          → Report · CriminalInfo · Attachment models + API
├── analytics/        → KPI computation, chart endpoints
└── media/            → uploaded files (audio, docs, images)
```

---

## API

<details>
<summary>Reports</summary>

| Method | Endpoint | Auth |
|---|---|---|
| `POST` | `/api/reports/` | Public |
| `GET` | `/api/reports/` | Required |
| `GET` | `/api/reports/track/<code>/` | Public |
| `GET` | `/api/reports/archive/` | Required |
| `PATCH` | `/api/reports/<id>/` | Admin · Employee |
| `DELETE` | `/api/reports/<id>/` | Admin · Employee |

</details>

<details>
<summary>Analytics</summary>

| Method | Endpoint | Auth |
|---|---|---|
| `GET` | `/analytics/stats/` | Required |
| `GET` | `/analytics/recent/` | Required |
| `GET` | `/analytics/site_stats/` | Public |

</details>

<details>
<summary>Accounts</summary>

| Method | Endpoint | Auth |
|---|---|---|
| `POST` | `/auth/login/` | Public |
| `POST` | `/auth/refresh/` | Public |
| `POST` | `/auth/password_reset/` | Public |
| `POST` | `/auth/password_reset_confirm/<uid>/<token>/` | Public |
| `GET · PATCH` | `/account/` | Active user |
| `GET · POST · PATCH · DELETE` | `/users/` | Admin only |

</details>

→ Full request/response examples: [`docs/api/`](docs/api/)

---

## Report Lifecycle

```
Submitted → Received → Under Review → In Progress ┬→ Solved ─→ Archive
                                                   └→ Closed ─→ Archive
```

---

## Quick Start

```bash
git clone https://github.com/salmakhalill/SecureReport_django.git
cd SecureReport_django

python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env   # SECRET_KEY · DEBUG · SENDGRID_API_KEY · DEFAULT_FROM_EMAIL

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

→ Full setup guide + AI classifier instructions: [`docs/setup.md`](docs/setup.md)

---

## Documentation

| | |
|---|---|
| [`docs/api/`](docs/api/) | Endpoint reference — request/response examples for all three apps |
| [`docs/database/erd.md`](docs/database/erd.md) | Entity relationship diagram |
| [`docs/database/data-dictionary.md`](docs/database/data-dictionary.md) | Field reference for all models |
| [`docs/architecture.md`](docs/architecture.md) | Technical decisions and trade-offs |
| [`docs/setup.md`](docs/setup.md) | Local setup, AI classifier, troubleshooting |

---

<div align="center">
<sub>Digitopia 2025 · Phase 3 of 4 · Egypt 🇪🇬</sub>
</div>
