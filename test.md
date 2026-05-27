<div align="center">

# 🛡️ SecureReport

![Django](https://img.shields.io/badge/Django-5.2-092E20?style=flat-square&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-3.x-ff1709?style=flat-square&logo=django&logoColor=white)
![JWT](https://img.shields.io/badge/Auth-JWT-black?style=flat-square&logo=jsonwebtokens&logoColor=white)
![React](https://img.shields.io/badge/Frontend-React-61DAFB?style=flat-square&logo=react&logoColor=black)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white)
![SendGrid](https://img.shields.io/badge/Email-SendGrid-1A82E2?style=flat-square&logo=sendgrid&logoColor=white)
![PythonAnywhere](https://img.shields.io/badge/Deploy-PythonAnywhere-1D9FD7?style=flat-square)

<br/>

🏆 **Digitopia 2025** — Phase 3 of 4 · Cybersecurity & AI track  
National ICT Competition · Ministry of Communications, Egypt

**Live API →** `https://salmakhalill.pythonanywhere.com`

</div>

---

Most people who witness a crime don't report it — not because they don't care, but because they're scared of being identified. SecureReport is built around that reality.

No account. No identity. Fill out the form, get a tracking code, and follow your case through a live status timeline.

On the other side, the authority receiving those reports gets a full dashboard to manage cases, update statuses, and track trends through analytics.

> **This repo is the backend only.**  
> Two React frontends were built by a teammate. I owned the API design, database, analytics module, deployment, and all the integration work that connected both sides together.

---

## Screenshots

| Public portal — status timeline | Authority dashboard |
|---|---|
| ![Tracking](docs/screenshots/tracking-timeline.png) | ![Dashboard](docs/screenshots/dashboard-analytics.png) |

<div align="center">
<br/>
<img src="docs/screenshots/welcome-email.png" width="500"/>
<br/><sub>Welcome email — sent automatically when a new staff account is created</sub>
</div>

---

## Features

**Public portal**

Reporters submit anonymously — location, incident date, description, suspect details, and file attachments. Audio files (`.mp3 .wav .webm .ogg`) are stored separately from other uploads. On submit, a unique 12-character tracking code is generated. Enter it later to see the case status through a visual timeline.

**Authority dashboard**

JWT login with three roles — Admin, Employee, and Viewer. KPI cards show total reports, new ones, under review, and critical cases, each with a trend indicator comparing current period to previous. Analytics charts have a daily / weekly / monthly toggle and are filterable by year. A geographic heatmap shows where incidents are concentrated. Reports move to the archive tab automatically when closed or solved.

**AI severity classifier** *(local only)*

Fine-tuned Arabic BERT model — predicts حرج / عالية / متوسطة / منخفضة at submission time. Not deployed because the weights (~400MB) are too large for PythonAnywhere. The `severity` field stays on the model; staff can set it manually, and there's a backfill script in `reports/ml_model.py`.

---

## Tech stack

| | |
|---|---|
| Framework | Django 5.2 + Django REST Framework |
| Auth | SimpleJWT — 1h access, 7d refresh |
| Database | SQLite |
| Analytics | Pandas · NumPy |
| AI | HuggingFace Transformers — Arabic BERT (local) |
| Email | SendGrid |
| Sanitization | bleach |
| Deployment | PythonAnywhere |

SQLite is in production because PythonAnywhere's free tier doesn't support external connections — PostgreSQL config is in the settings file, commented out. Analytics uses Pandas instead of ORM aggregations because the KPI logic came from Power BI specs and mapped cleanly onto DataFrame operations.

---

## Project structure

```
accounts/   auth, roles, user management, password reset, SendGrid
reports/    Report · CriminalInfo · Attachment — models, serializers, views
analytics/  KPI computation and chart endpoints — read-only, never writes to DB
config/     settings, root URLs
media/      uploaded files — audio/ and files/ subdirectories
```

---

## API

<details>
<summary><b>Reports</b></summary>
<br/>

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
<summary><b>Analytics</b></summary>
<br/>

| Method | Endpoint | Auth |
|---|---|---|
| `GET` | `/analytics/recent/` | Required |
| `GET` | `/analytics/stats/` | Required |
| `GET` | `/analytics/site_stats/` | Public |

</details>

<details>
<summary><b>Accounts</b></summary>
<br/>

| Method | Endpoint | Auth |
|---|---|---|
| `POST` | `/auth/login/` | Public |
| `POST` | `/auth/refresh/` | Public |
| `POST` | `/auth/password_reset/` | Public |
| `POST` | `/auth/password_reset_confirm/<uid>/<token>/` | Public |
| `GET · PATCH` | `/account/` | Active user |
| `GET · POST · PATCH · DELETE` | `/users/` | Admin only |

</details>

Full request/response reference → [`docs/api/`](docs/api/)

---

## Report lifecycle

```
Submitted → Received → Under Review → In Progress ┬→ Solved ──→ Archive
                                                   └→ Closed ──→ Archive
```

---

## Quick start

```bash
git clone https://github.com/salmakhalill/SecureReport_django.git
cd SecureReport_django
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate && python manage.py createsuperuser
python manage.py runserver
```

`.env` variables: `SECRET_KEY` · `DEBUG` · `SENDGRID_API_KEY` · `DEFAULT_FROM_EMAIL`

Full guide with troubleshooting and AI classifier setup → [`docs/setup.md`](docs/setup.md)

---

## Documentation

| | |
|---|---|
| [`docs/api/`](docs/api/) | Full endpoint reference with request/response examples |
| [`docs/database/erd.md`](docs/database/erd.md) | Entity relationship diagram |
| [`docs/database/data-dictionary.md`](docs/database/data-dictionary.md) | Field reference for all models |
| [`docs/sequence-diagrams.md`](docs/sequence-diagrams.md) | Submission, tracking, and password reset flows |
| [`docs/class-diagram.md`](docs/class-diagram.md) | Model relationships |
| [`docs/architecture.md`](docs/architecture.md) | Technical decisions and trade-offs |
| [`docs/setup.md`](docs/setup.md) | Local setup + troubleshooting |

---

<div align="center">
<sub>Digitopia 2025 · Phase 3 of 4 · Egypt 🇪🇬</sub>
</div>
