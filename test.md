# Reports API

`Base URL: https://salmakhalill.pythonanywhere.com/api`

---

### `POST /reports/` — submit a report

Public. No authentication required. Accepts `multipart/form-data` because the request carries file uploads.

**Fields:**

| Field | Required | Notes |
|---|---|---|
| `location` | yes | Human-readable location name |
| `incident_date` | yes | `YYYY-MM-DD` |
| `report_details` | yes | Sanitized with bleach before saving |
| `report_type` | yes | `اعتداء` · `ابتزاز` · `تحرش` · `سرقة` · `مشادة` |
| `location_link` | no | Any map URL |
| `latitude` / `longitude` | no | GPS coordinates |
| `contact_info` | no | Optional — reporter's choice |
| `criminal_infos` | no | JSON string (see below) |
| `attachments` | no | Audio: `.mp3 .wav .webm .ogg` — everything else → files |

`criminal_infos` is sent as a JSON string inside the form field:
```json
[{ "name": "...", "description": "...", "other_info": "..." }]
```

**Response `201`:**
```json
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
  "report_details": "...",
  "contact_info": null,
  "severity": null,
  "criminal_infos": [{ "name": "...", "description": "...", "other_info": null }],
  "attachments": [{ "type": "audio", "url": "https://.../media/attachments/audio/rec.webm" }],
  "created_at": "2025-08-10T14:32:00Z"
}
```

`severity` is null on creation — set by the AI classifier locally or manually by staff.

---

### `GET /reports/` — list active reports

Requires authentication. Excludes `تم الحل` and `تم الإغلاق` — those are in the archive.

Admins and Employees get the full object. Viewers only see `id · tracking_code · status · report_type · created_at`.

---

### `GET /reports/track/<tracking_code>/` — track a report

Public. Returns minimal fields — enough to drive the status timeline on the public portal.

```json
{
  "id": 42,
  "tracking_code": "A1B2C3D4E5F6",
  "status": "قيد المعالجة",
  "report_type": "تحرش",
  "created_at": "2025-08-10T14:32:00Z"
}
```

Returns `404` if the code doesn't exist.

---

### `GET /reports/archive/`

Requires authentication. Returns only `تم الحل` and `تم الإغلاق` reports. Same field split by role as the list endpoint.

---

### `PATCH /reports/<id>/` — update a report

Admin and Employee only. Partial update — send any subset of fields.

```json
{ "status": "قيد المراجعة", "severity": "حرج" }
```

Returns `403` for Viewers or inactive users.

---

### `DELETE /reports/<id>/`

Admin and Employee only. Returns `204`.
