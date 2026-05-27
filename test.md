# Architecture & Technical Decisions

---

## Project Structure

SecureReport is a Django monolith split into three apps, each with a single responsibility:

```
accounts/    → identity: who you are, authentication, permissions
reports/     → core domain: what gets reported, by whom (anonymous), in what state
analytics/   → read layer: how reports are aggregated and surfaced to the dashboard
```

This separation means analytics never writes to the database — it only reads. Reports never touch auth logic. The apps only communicate through model imports, not circular dependencies.

---

## Why Django REST Framework

The two frontends (public portal and authority dashboard) are separate React apps on separate domains. A REST API is the only sensible interface between them and the backend — it decouples deployment, lets the frontend iterate independently, and is easy to test with any HTTP client.

DRF was chosen over alternatives like FastAPI because the project already uses Django's ORM, admin, and auth system. Adding DRF has near-zero overhead in that context, and the serializer/view pattern fits well with nested models like `Report → CriminalInfo + Attachments`.

---

## Why JWT Authentication

Dashboard users need to stay logged in across sessions without the server storing session state. JWT satisfies that:

- Access token (1 hour) — short-lived, used for every request
- Refresh token (7 days) — used only to get a new access token, stored securely by the frontend

The custom login serializer (`MyTokenObtainPairSerializer`) adds `role`, `email`, and `status` to the token response so the frontend can gate UI elements immediately without a separate `/me/` call.

---

## Why the Public Portal Has No Auth

Anonymous reporting is the entire point. Requiring registration would defeat the purpose — people don't report crimes because they don't want to be identified. The trade-off is that anyone can submit a report, including fake ones. This is handled by the `is_fake` flag on the Report model, which staff can set manually.

---

## Role System Design

Three roles cover the real-world access pattern of a government reporting system:

- **Admin** — the system owner. Manages staff accounts, sees everything, can delete.
- **Employee** — a case worker. Can update and close cases but can't touch user accounts.
- **Viewer** — an observer (e.g. a partner organization). Read-only, and even then sees only non-sensitive fields.

The `status` field on `CustomUser` is separate from `is_active`. `status = 'inactive'` means the account exists but the person shouldn't be accessing live data — used when someone leaves the organization without deleting their account. All views check `status == 'active'` before returning any data.

---

## Report Lifecycle & Archive Split

Active reports and archived reports are served from different endpoints (`/reports/` vs `/reports/archive/`) rather than using a query param. This is intentional:

- The dashboard's "active cases" view never accidentally shows closed cases
- Archive is a separate tab — a separate concern
- The split is enforced in `get_queryset()`, not in the frontend

Status transitions that move a report to archive: `تم الحل` and `تم الإغلاق`. These are set manually by staff via `PATCH /reports/<id>/`.

---

## Analytics: Pandas Over Raw SQL

The analytics module uses Pandas DataFrames instead of Django ORM aggregations. The reason: the KPI calculations involve time-bucketing, rolling comparisons (current period vs previous period), and Arabic label mapping — logic that would be verbose and hard to read as ORM annotations.

The Power BI specs provided by the data analyst defined the KPI formulas and chart structures. These were translated into Pandas operations in `utils.py`. The result is a clean separation: Django handles persistence, Pandas handles computation.

One known trade-off: loading all reports into a DataFrame on every request doesn't scale beyond tens of thousands of rows. For the current dataset size this is acceptable. A production-scale version would use database-level aggregations or a caching layer.

---

## Why SQLite in Production

PythonAnywhere's free tier doesn't support external database connections. SQLite is sufficient for the current data volume and access pattern (mostly reads, infrequent writes). The settings file includes the scaffolding to switch to PostgreSQL via `DATABASE_URL` (commented out) when the project moves to a paid environment.

---

## Security Hardening

Production settings (active when `DEBUG=False`) add:

| Setting | Purpose |
|---|---|
| `SECURE_SSL_REDIRECT` | Force HTTPS on all requests |
| `SESSION_COOKIE_SECURE` | Session cookie only over HTTPS |
| `CSRF_COOKIE_SECURE` | CSRF cookie only over HTTPS |
| `SESSION_COOKIE_HTTPONLY` | Block JS access to session cookie |
| `X_FRAME_OPTIONS = DENY` | Prevent clickjacking |
| `SECURE_CONTENT_TYPE_NOSNIFF` | Prevent MIME type sniffing |
| `SECURE_BROWSER_XSS_FILTER` | Enable browser XSS protection header |

Input from anonymous reporters is sanitized with `bleach` (strips all HTML tags) on `location`, `report_details`, and `contact_info` before hitting the database.

---

## Email: SendGrid over SMTP

SendGrid was chosen over direct SMTP (Gmail) because:
- No app-password workarounds needed
- Better deliverability
- HTML templates render reliably

Two transactional emails exist: welcome (new staff account with password-setup link) and password reset. Both use Django's token generator (`default_token_generator`) which produces single-use, time-limited tokens tied to the user's current password hash.

---

## AI Classifier (Local Only)

A fine-tuned Arabic BERT model predicts report severity at submission time. It's excluded from the deployed version because the model weights (~400MB) exceed what PythonAnywhere can load in a web worker.

The call in `views.py` is commented out with a clear note. The `severity` field remains on the model and can be set manually by staff in the meantime. The backfill script in `ml_model.py` can be run locally against the production database when needed.
