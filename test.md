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

🏆 **Digitopia 2025** — reached Phase 3 of 4, Cybersecurity & AI track  
National ICT Competition · Ministry of Communications, Egypt

**Live API:** `https://salmakhalill.pythonanywhere.com`

</div>

---

Most people who witness a crime don't report it — not because they don't care, but because they're scared of being identified. SecureReport is built around that. You fill out a form, get a tracking code, and that's it. No account, no identity, just a code to follow your case.

On the other side there's a dashboard where the receiving authority logs in, manages incoming cases, and monitors trends through analytics charts.

> **This repo is the backend only.**  
> The two React frontends were built by a teammate. My role was the API, database design, analytics module, deployment on PythonAnywhere, and all the integration work connecting backend to frontend.

---

## Screenshots

| Public portal — tracking timeline | Authority dashboard |
|---|---|
| ![Tracking](docs/screenshots/tracking-timeline.png) | ![Dashboard](docs/screenshots/dashboard-analytics.png) |

<div align="center">
<br/>
<img src="docs/screenshots/welcome-email.png" width="500"/>
<br/><sub>Welcome email — sent automatically when a new staff account is created</sub>
</div>

---

## Public portal

Anyone can submit a report — no registration. The form takes location (with optional map link and GPS coordinates), incident date, description, suspect info, and file attachments. Audio files are stored separately from other uploads. On submit, a 12-character tracking code is generated and shown once — the reporter uses it later to check their case status through a visual timeline.

## Authority dashboard

Staff log in with JWT. There are three roles: Admin can do everything including managing other users. Employee handles cases but can't touch accounts. Viewer gets read-only access with limited fields.

The dashboard has KPI cards with trend comparisons (total reports, new, under review, critical), analytics charts with a daily/weekly/monthly toggle filterable by year, a geographic heatmap, and a reports table where staff update case status. When a case is marked solved or closed it automatically moves to the archive tab.

Password reset works via email. When an admin creates a new user, a welcome email goes out with a link to set their password — no temporary passwords floating around.

## AI severity classifier *(not deployed)*

There's a fine-tuned Arabic BERT model that predicts report severity at submission: حرج / عالية / متوسطة / منخفضة. The model weights (~400MB) are too large for PythonAnywhere, so the inference call is commented out in `views.py`. The `severity` field stays on the model and staff can set it manually. There's a backfill script in `reports/ml_model.py` for running it locally when needed.

---

## Tech stack

| | |
|---|---|
| Framework | Django 5.2 + Django REST Framework |
| Auth | SimpleJWT — 1h access token, 7d refresh |
| Database | SQLite |
| Analytics | Pandas + NumPy |
| AI | HuggingFace Transformers, Arabic BERT (local only) |
| Email | SendGrid |
| Input sanitization | bleach |
| Deployment | PythonAnywhere |

SQLite is in production because PythonAnywhere's free tier doesn't support external DB connections — the settings file has the PostgreSQL config commented out for when that changes. The analytics module uses Pandas instead of ORM aggregations because the KPI formulas came from Power BI specs and translated naturally into DataFrame operations.

---

## Project structure

```
accounts/   auth, roles, users, password reset, SendGrid
reports/    Report · CriminalInfo · Attachment — models, serializers, views
analytics/  KPI computation and chart endpoints (read-only, never writes)
config/     settings, root URLs
media/      uploaded files — audio/ and files/ subdirectories
```

---

## API

<details>
<summary>Reports</summary>
<br/>

| Method | Endpoint | Auth |
|---|---|---|
| `POST` | `/api/reports/` | public |
| `GET` | `/api/reports/` | required |
| `GET` | `/api/reports/track/<code>/` | public |
| `GET` | `/api/reports/archive/` | required |
| `PATCH` | `/api/reports/<id>/` | Admin, Employee |
| `DELETE` | `/api/reports/<id>/` | Admin, Employee |

</details>

<details>
<summary>Analytics</summary>
<br/>

| Method | Endpoint | Auth |
|---|---|---|
| `GET` | `/analytics/recent/` | required |
| `GET` | `/analytics/stats/` | required |
| `GET` | `/analytics/site_stats/` | public |

</details>

<details>
<summary>Accounts</summary>
<br/>

| Method | Endpoint | Auth |
|---|---|---|
| `POST` | `/auth/login/` | public |
| `POST` | `/auth/refresh/` | public |
| `POST` | `/auth/password_reset/` | public |
| `POST` | `/auth/password_reset_confirm/<uid>/<token>/` | public |
| `GET · PATCH` | `/account/` | active user |
| `GET · POST · PATCH · DELETE` | `/users/` | Admin only |

</details>

Full request/response examples → [`docs/api/`](docs/api/)

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

`.env` needs `SECRET_KEY` · `DEBUG` · `SENDGRID_API_KEY` · `DEFAULT_FROM_EMAIL`  
Full setup guide with troubleshooting → [`docs/setup.md`](docs/setup.md)

---

## Docs

| | |
|---|---|
| [`docs/api/`](docs/api/) | Endpoint reference — full request/response for all three apps |
| [`docs/database/erd.md`](docs/database/erd.md) | Entity relationship diagram |
| [`docs/database/data-dictionary.md`](docs/database/data-dictionary.md) | Field reference for all models |
| [`docs/sequence-diagrams.md`](docs/sequence-diagrams.md) | Auth, submission, password reset flows |
| [`docs/class-diagram.md`](docs/class-diagram.md) | Model relationships |
| [`docs/architecture.md`](docs/architecture.md) | Technical decisions and trade-offs |
| [`docs/setup.md`](docs/setup.md) | Local setup + troubleshooting |

---

<div align="center">
<sub>Digitopia 2025 · Phase 3 of 4 · Egypt 🇪🇬</sub>
</div>
