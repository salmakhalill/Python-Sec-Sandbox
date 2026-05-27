# Reports API

Base URL: `https://salmakhalill.pythonanywhere.com/api`

---

## POST `/reports/`

Submit an anonymous report.

Public endpoint — no authentication required.

**Content-Type:** `multipart/form-data`  
Reports may include audio recordings, documents, or images.

### Request Fields

| Field | Type | Required | Notes |
|---|---|---|---|
| `location` | string | yes | Human-readable location |
| `location_link` | string | no | Any map URL |
| `latitude` | decimal | no | GPS latitude |
| `longitude` | decimal | no | GPS longitude |
| `incident_date` | date | yes | Format: `YYYY-MM-DD` |
| `report_details` | string | yes | Sanitized with `bleach` before saving |
| `contact_info` | string | no | Optional — reporter's choice |
| `report_type` | string | yes | `اعتداء` · `ابتزاز` · `تحرش` · `سرقة` · `مشادة` |
| `criminal_infos` | JSON string | no | Array of criminal objects |
| `attachments` | file(s) | no | Audio: `.mp3 .wav .webm .ogg` |

All non-audio uploads are treated as generic files.

### `criminal_infos` Format

Sent as a JSON string inside the form field:

```json
[
  {
    "name": "اسم المشتبه به",
    "description": "وصف مختصر",
    "other_info": "معلومات إضافية"
  }
]
Response 201
{
  "id": 42,
  "tracking_code": "A1B2C3D4E5F6",
  "status": "تم استلام البلاغ",
  "location": "القاهرة، شارع التحرير",
  "latitude": "30.044420000000000",
  "longitude": "31.235710000000000",
  "location_link": "https://maps.google.com/?q=...",
  "report_type": "تحرش",
  "incident_date": "2025-08-10",
  "report_details": "تفاصيل الحادثة...",
  "contact_info": null,
  "severity": null,
  "criminal_infos": [
    {
      "name": "اسم المشتبه به",
      "description": "وصف مختصر",
      "other_info": null
    }
  ],
  "attachments": [
    {
      "type": "audio",
      "url": "https://salmakhalill.pythonanywhere.com/media/attachments/audio/recording.webm"
    }
  ],
  "created_at": "2025-08-10T14:32:00Z"
}

severity is null on creation — populated later by the local AI classifier or manually by staff.

GET /reports/

List active reports.

Requires authentication.

Reports with status تم الحل and تم الإغلاق are excluded from this endpoint and served from /reports/archive/.

Headers
Authorization: Bearer <access_token>
Role-Based Response Behavior
Admin / Employee → receive the full report object
Viewer → limited fields only:
id · tracking_code · status · report_type · created_at
Response 200 — Admin / Employee
[
  {
    "id": 42,
    "tracking_code": "A1B2C3D4E5F6",
    "status": "قيد المراجعة",
    "location": "القاهرة، شارع التحرير",
    "report_type": "تحرش",
    "incident_date": "2025-08-10",
    "report_details": "...",
    "severity": "عالية",
    "criminal_infos": [...],
    "attachments": [...],
    "created_at": "2025-08-10T14:32:00Z"
  }
]
Response 200 — Viewer
[
  {
    "id": 42,
    "tracking_code": "A1B2C3D4E5F6",
    "status": "قيد المراجعة",
    "report_type": "تحرش",
    "created_at": "2025-08-10T14:32:00Z"
  }
]
Response 403
{
  "detail": "Permission denied."
}

Inactive users receive empty responses regardless of role.

GET /reports/track/<tracking_code>/

Track a report using its public tracking code.

Public endpoint — no authentication required.

Returns minimal fields required for the public status timeline.

Example
GET /reports/track/A1B2C3D4E5F6/
Response 200
{
  "id": 42,
  "tracking_code": "A1B2C3D4E5F6",
  "status": "قيد المعالجة",
  "report_type": "تحرش",
  "created_at": "2025-08-10T14:32:00Z"
}
Response 404
{
  "detail": "Not found."
}
GET /reports/archive/

List archived reports.

Requires authentication.

Only reports with status:

تم الحل
تم الإغلاق

Same role-based field restrictions as GET /reports/.

Headers
Authorization: Bearer <access_token>
PATCH /reports/<id>/

Partially update a report.

Admin and Employee only.

Headers
Authorization: Bearer <access_token>
Request Body

Any subset of fields may be sent.

{
  "status": "قيد المراجعة",
  "severity": "حرج"
}
Response 200

Returns the updated report object.

Response 403
{
  "detail": "Permission denied."
}
DELETE /reports/<id>/

Delete a report.

Admin and Employee only.

Headers
Authorization: Bearer <access_token>
Response 204

No content.

Response 403
{
  "detail": "Permission denied."
}
