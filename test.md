# Data Dictionary

---

## Report

The core table. One row per submitted report.

| Field | Type | Notes |
|---|---|---|
| `id` | Integer | PK |
| `tracking_code` | CharField(12) | Auto-generated on first save, never changes |
| `location` | CharField(255) | Human-readable name |
| `location_link` | URLField | Optional map URL |
| `latitude` / `longitude` | Decimal(18,15) | Optional GPS |
| `incident_date` | DateField | Date of incident — not submission date |
| `report_details` | TextField | Sanitized with bleach before saving |
| `contact_info` | CharField(255) | Optional, reporter's choice |
| `report_type` | CharField | `اعتداء` · `ابتزاز` · `تحرش` · `سرقة` · `مشادة` |
| `status` | CharField | Default: `تم استلام البلاغ` |
| `severity` | CharField | `حرج` · `عالية` · `متوسطة` · `منخفضة` — set by AI or manually |
| `is_fake` | Boolean | Default false — staff flag for suspicious reports |
| `created_at` | DateTimeField | Auto, submission timestamp |

Status flow: `تم استلام البلاغ` → `قيد المراجعة` → `قيد المعالجة` → `تم الحل` / `تم الإغلاق`

Reports in `تم الحل` or `تم الإغلاق` are excluded from `GET /api/reports/` and only surface in `/api/reports/archive/`.

---

## CriminalInfo

Suspect details linked to a report. One report can have zero or more.

| Field | Type | Notes |
|---|---|---|
| `id` | Integer | PK |
| `report` | FK → Report | Cascade delete |
| `name` | CharField(255) | |
| `description` | TextField | Optional — physical description, identifying details |
| `other_info` | TextField | Optional |

---

## Attachment

Files uploaded with a report. Classified by extension at upload time — audio goes to `media/attachments/audio/`, everything else to `media/attachments/files/`.

Audio extensions: `.mp3 .wav .webm .ogg`

| Field | Type | Notes |
|---|---|---|
| `id` | Integer | PK |
| `report` | FK → Report | Cascade delete |
| `audio_recording` | FileField | Populated for audio |
| `file` | FileField | Populated for everything else |

Each row has one field populated, never both.

---

## CustomUser

Staff accounts only. Reporters are fully anonymous and have no user record.

| Field | Type | Notes |
|---|---|---|
| `id` | Integer | PK |
| `email` | EmailField | Unique — used as login username |
| `full_name` | CharField(255) | Optional |
| `role` | CharField | `Admin` · `Employee` · `Viewer` (default: Viewer) |
| `status` | CharField | `Active` · `Inactive` (default: active) |
| `date_joined` | DateTimeField | Auto |
| `is_staff` | Boolean | Django admin access |
| `is_active` | Boolean | Django built-in, separate from `status` |
| `password` | CharField | Hashed — set via welcome email on first login |

`status` and `is_active` serve different purposes. `is_active=False` blocks at the Django auth layer. `status='inactive'` is the application-level check enforced in every view — the clean way to revoke access without deleting the account.
