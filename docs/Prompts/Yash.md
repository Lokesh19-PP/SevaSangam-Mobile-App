# Yash — Antigravity Prompt Pack (SevaSangam Backend API)

**You own:** FastAPI app structure, auth + RBAC, and the core REST endpoints (`/api/v1/...`).

**Wait for Lokesh's Prompts 1–3** (Docker/Postgres/PostGIS + core models) to be merged before starting — every endpoint here reads/writes through his models. You can work in parallel with Yash-Thakur once the schema lands.

Before every prompt: paste `docs/ANTIGRAVITY_CONTEXT.md` as the first message in a new session, then paste the numbered prompt. Keep `docs/api/DB_SCHEMA.md` (Lokesh) open for field names.

---

### Prompt 1 — FastAPI app scaffold
```
Scaffold backend/app/: main.py (FastAPI app, CORS for the mobile app's dev origins, versioned router mount at /api/v1), app/api/v1/ router package, app/core/config.py (Pydantic Settings reading env vars — DB URL, JWT secret, mock/OTP toggle), app/db/session.py (SQLAlchemy session dependency). Add a health check endpoint. Confirm it boots with uvicorn and serves interactive OpenAPI docs at /docs.
```
**Commit:** `feat(api): scaffold FastAPI app with versioned router, config and DB session dependency`

---

### Prompt 2 — Auth: phone OTP + JWT + RBAC
```
Build app/api/v1/auth.py: POST /auth/request-otp (mock — accepts any Indian phone number, "sends" a fixed OTP like 123456 in dev mode, logs it instead of calling Twilio), POST /auth/verify-otp (issues a JWT with user id + role claim), POST /auth/select-role (Customer/Worker only — Admin can NEVER be selected here, matching the mobile RoleSelect rule exactly). Build app/core/security.py: JWT creation/verification and a get_current_user dependency, plus a require_role(*roles) dependency factory for RBAC. Admin-namespaced routes (built later) will use require_role("admin").
```
**Commit:** `feat(api): add phone-OTP auth flow with JWT issuance and RBAC dependency`

---

### Prompt 3 — Users & Cooperatives endpoints
```
Build app/api/v1/users.py (GET/PATCH current user profile, admin-only list) and app/api/v1/cooperatives.py (list, detail). Response schemas import from Lokesh's Pydantic schemas — do not redefine field shapes. Add pagination (page/limit) on list endpoints per the mobile contract in section 7 of the mobile context doc.
```
**Commit:** `feat(api): add Users and Cooperatives endpoints with pagination`

---

### Prompt 4 — Workers endpoints
```
Build app/api/v1/workers.py: GET /workers (list with skill/distance/availability/cooperative/rating filters using Lokesh's geo-query helpers — never duplicate the PostGIS query), GET /workers/{id}, PATCH /workers/{id} (self-update: availability toggle, skills, service area), POST /workers/{id}/certificates (upload endpoint — accept the image, store a reference, mark status "pending"; actual OCR wiring happens in Yash-Thakur's prompt, stub the OCR call for now behind a TODO). Enforce that a worker can only PATCH their own record.
```
**Commit:** `feat(api): add Workers endpoints with geo/skill filtering and self-update`

---

### Prompt 5 — Service categories & Bookings endpoints
```
Build app/api/v1/service_categories.py (list). Build app/api/v1/bookings.py: POST /bookings (scheduled and emergency booking creation — call into a matching_service placeholder function that Yash-Thakur will implement, stub it to just pick the nearest available worker via Lokesh's geo helper for now), GET /bookings (role-aware: customer sees their own, worker sees assigned, filters for status/type/date), GET /bookings/{id}, PATCH /bookings/{id}/status (enforce valid status transitions per the enum in the mobile context — reject illegal transitions with a 400). Every state change should be appendable to a timeline field/table for the mobile booking-tracking UI.
```
**Commit:** `feat(api): add Service Categories and Bookings endpoints with status-transition validation`

---

### Prompt 6 — Reviews endpoint
```
Build app/api/v1/reviews.py: POST /reviews (only for completed bookings the requesting customer owns, one review per booking enforced), GET /workers/{id}/reviews (paginated). Update the worker's rating/ratingCount aggregate on new review creation (simple running average is fine for MVP).
```
**Commit:** `feat(api): add Reviews endpoint with one-review-per-booking enforcement and rating aggregation`

---

### Prompt 7 — Admin-namespaced endpoints (Part 1: verification + workers)
```
Build app/api/v1/admin/verification.py (GET pending queue, POST approve/reject-with-reason/request-reupload) and app/api/v1/admin/workers.py (list with filters, suspend/reactivate). Every route here uses require_role("admin"). Mirror the exact mock-mode behavior the mobile app expects per section 7 of the mobile context: reject non-admin callers the same way the mock does.
```
**Commit:** `feat(api): add admin Verification and Workers management endpoints`

---

### Prompt 8 — Admin-namespaced endpoints (Part 2: bookings, complaints, welfare)
```
Build app/api/v1/admin/bookings.py (monitor list with filters, manual reassign action), app/api/v1/admin/complaints.py (list by status, start-review/add-note/resolve/reject), app/api/v1/admin/welfare.py (CRUD for welfare programmes, announce-to-workers as a stub notification trigger).
```
**Commit:** `feat(api): add admin Bookings monitor, Complaints and Welfare Programmes endpoints`

---

### Prompt 9 — Notifications endpoint (stub)
```
Build app/api/v1/notifications.py: GET (paginated, role-aware), PATCH mark-as-read. Real push is out of scope (stubbed on both mobile and backend per section 18 of the mobile context) — this just persists/serves Notification rows that other endpoints create (e.g. new job request, new emergency, verification result).
```
**Commit:** `feat(api): add Notifications endpoint (read/mark-as-read, push stays stubbed)`

---

### Prompt 10 — Contract reconciliation pass
```
Compare every endpoint's request/response shape against docs/api/MOBILE_API_REQUESTS.md and the mobile app's services/api/*.js function signatures (ask for those files or read them from the repo). List every mismatch (field name, missing filter param, wrong pagination shape) as resolved/needs-discussion entries in MOBILE_API_REQUESTS.md, and fix the ones that are clearly bugs on the API side now.
```
**Commit:** `docs(api): reconcile endpoint contracts against mobile API requests log`