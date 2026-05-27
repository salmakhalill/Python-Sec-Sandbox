# Data Dictionary

## Report

The main table. One row per submitted report.

| Field | Type | Required | Notes |
|---|---|---|---|
| `id` | Integer | auto | Primary key |
| `tracking_code` | CharField(12) | auto | Unique, auto-generated UUID hex on save. Used by reporters to track their case. |
| `location` | CharField(255) | yes | Human-readable location name |
| `location_link` | URLField | no | Optional Google Maps or any map URL |
| `latitude` | Decimal(18,15) | no | GPS latitude |
| `longitude` | Decimal(18,15) | no | GPS longitude |
| `incident_date` | DateField | yes | Date the incident occurred (not submission date) |
| `report_details` | TextField | yes | Full description of the incident. Sanitized with bleach on input. |
| `contact_info` | CharField(255) | no | Optional — reporter may leave a way to be contacted |
| `report_type` | CharField | yes | One of: اعتداء · ابتزاز · تحرش · سرقة · مشادة |
| `status` | CharField | auto | One of: تم استلام البلاغ · قيد المراجعة · قيد المعالجة · تم الحل · تم الإغلاق. Default: تم استلام البلاغ |
| `severity` | CharField | no | One of: حرج · عالية · متوسطة · منخفضة. Set by AI classifier or manually by staff. |
| `is_fake` | Boolean | auto | Default false. Flag for staff to mark suspicious reports. |
| `created_at` | DateTimeField | auto | Submission timestamp |

**Notes:**
- Reports with status `تم الحل` or `تم الإغلاق` are excluded from the active reports list and appear in the archive endpoint instead.
- `tracking_code` is generated once on first save and never changes.

---

## CriminalInfo

Information about a suspect linked to a report. A report can have multiple suspects.

| Field | Type | Required | Notes |
|---|---|---|---|
| `id` | Integer | auto | Primary key |
| `report` | ForeignKey → Report | yes | Cascade delete |
| `name` | CharField(255) | yes | Suspect name |
| `description` | TextField | no | Physical description or identifying details |
| `other_info` | TextField | no | Any additional information |

---

## Attachment

Files uploaded with a report. A report can have multiple attachments.

| Field | Type | Required | Notes |
|---|---|---|---|
| `id` | Integer | auto | Primary key |
| `report` | ForeignKey → Report | yes | Cascade delete |
| `audio_recording` | FileField | no | Stored under `media/attachments/audio/`. Detected by extension: .mp3 .wav .webm .ogg |
| `file` | FileField | no | Stored under `media/attachments/files/`. All other file types. |

**Note:** Each Attachment row holds either `audio_recording` or `file`, not both.

---

## CustomUser

Custom user model replacing Django's default. Used for dashboard staff accounts only — reporters are anonymous.

| Field | Type | Required | Notes |
|---|---|---|---|
| `id` | Integer | auto | Primary key |
| `email` | EmailField | yes | Unique. Used as the login username. |
| `full_name` | CharField(255) | no | Display name |
| `role` | CharField | yes | One of: Admin · Employee · Viewer. Default: Viewer |
| `status` | CharField | yes | One of: Active · Inactive. Default: active. Inactive users cannot access any data. |
| `date_joined` | DateTimeField | auto | Account creation timestamp |
| `is_staff` | Boolean | auto | Required for Django admin access. True for superusers only. |
| `is_active` | Boolean | auto | Django-level flag. Distinct from `status` field above. |
| `password` | CharField | yes | Hashed. Set via welcome email link on first login. |

**Roles:**
- `Admin` — full access including user management
- `Employee` — can view, update, and delete reports. Cannot manage users.
- `Viewer` — read-only, sees limited report fields (tracking_code, status, type, date only)

---

## Relationships

```
CustomUser ──(manages)──> Report
Report ──1:N──> CriminalInfo
Report ──1:N──> Attachment
```
