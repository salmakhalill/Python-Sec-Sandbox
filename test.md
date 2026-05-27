# Accounts API

`Base URL: https://salmakhalill.pythonanywhere.com`

---

### `POST /auth/login/`

```json
{ "email": "admin@securereport.com", "password": "..." }
```

Returns JWT tokens and user info. The `role`, `email`, and `status` are included in the response so the frontend can gate UI elements immediately — no separate `/me/` call needed.

```json
{
  "access": "eyJ...",
  "refresh": "eyJ...",
  "role": "Admin",
  "email": "admin@securereport.com",
  "status": "active"
}
```

---

### `POST /auth/refresh/`

```json
{ "refresh": "eyJ..." }
```

Returns a new `access` token. Access tokens expire in 1 hour, refresh tokens in 7 days.

---

### Password reset

Two steps:

**1. Request the email**  
`POST /auth/password_reset/` → `{ "email": "..." }`

Always returns `200` even if the email doesn't exist — prevents user enumeration.

**2. Set the new password**  
`POST /auth/password_reset_confirm/<uidb64>/<token>/`

```json
{ "new_password": "...", "confirm_password": "..." }
```

The token is single-use and tied to the user's current password hash, so it invalidates automatically after the password changes. Returns `400` if expired or already used.

---

### `GET · PATCH /account/`

View or update the currently logged-in user's profile.

To change password, include both `current_password` and `new_password`. The endpoint verifies the current password before proceeding.

---

### User management — Admin only

**`GET /users/`** — list all staff accounts.

**`POST /users/`** — create a new user. No password needed in the request — one is auto-generated and a welcome email goes out with a setup link.

```json
{ "email": "...", "full_name": "...", "role": "Employee" }
```

**`PATCH /users/<id>/`** — update role or status. Setting `status: Inactive` blocks access without deleting the account.

**`DELETE /users/<id>/`** — returns `204`.
