# Lokesh — Antigravity Prompt Pack (SevaSangam Backend & Database)

**You own:** Docker/Postgres/PostGIS setup, database schema, migrations, seed data, geo-query helpers.

**You are the foundation for the backend trio.** Yash (API) and Yash-Thakur (AI/integrations) both build on top of your schema — get Prompts 1–3 merged and communicated before they start writing endpoints/models against it.

Before every prompt: open a new Antigravity session and paste the full contents of your team's `docs/ANTIGRAVITY_CONTEXT.md` (web/backend context doc) as the first message. Also keep `docs/ANTIGRAVITY_MOBILE_CONTEXT.md` section 7's entity table and enums open for reference — your schema's field names must match it exactly, since mobile mock data is built against those exact names.

---

### Prompt 1 — Docker + Postgres + PostGIS
```
Set up docker/docker-compose.yml (or extend the existing one) with a postgres service using the postgis/postgis image, exposed on the standard port, with a persistent volume and a healthcheck. Add backend/.env.example with DB connection vars. Add a short docs/api/DB_SETUP.md explaining how to bring the DB up locally and confirm PostGIS is enabled (CREATE EXTENSION postgis).
```
**Commit:** `chore(db): add Postgres+PostGIS service to docker-compose with setup docs`

---

### Prompt 2 — Core entity models (Part 1)
```
In backend/app/models/ (SQLAlchemy) and backend/app/schemas/ (Pydantic), create models + schemas for User, Cooperative, Worker (with a PostGIS Geography(Point) column for location, plus serviceRadiusKm, workloadThisWeek, insurance fields), and Certificate. Field names and types must match the entity table in docs/ANTIGRAVITY_MOBILE_CONTEXT.md section 7 exactly (id, userId, cooperativeId, skills[], experienceYears, rating, ratingCount, verificationStatus, availability, location{lat,lng}, etc. — translate camelCase mobile field names to snake_case DB columns consistently, and document the mapping). Use enums (not free text) for role, verificationStatus, availability, certificate status.
```
**Commit:** `feat(db): add User, Cooperative, Worker and Certificate models with PostGIS location column`

---

### Prompt 3 — Core entity models (Part 2)
```
Add models + schemas for ServiceCategory, Booking (status and type as enums matching the mobile context's provisional enum list exactly: pending→assigned→accepted→en_route→in_progress→completed, plus rejected/cancelled/unassigned; type scheduled|emergency), Review, Complaint, WelfareProgram, Earning, Notification. Keep field names aligned with the entity table. Add foreign keys and cascade rules that make sense (e.g. deleting a User should not silently delete their Bookings — decide and document the policy).
```
**Commit:** `feat(db): add ServiceCategory, Booking, Review, Complaint, WelfareProgram, Earning, Notification models`

---

### Prompt 4 — Alembic migrations + seed script
```
Set up Alembic in backend/, generate the initial migration covering all models from Prompts 2-3, and confirm it applies cleanly to a fresh Postgres+PostGIS container. Write a seed script (backend/scripts/seed_db.py or similar) that inserts realistic demo data: a few cooperatives, ~15 workers across different skills/locations/availability/verification states (including at least one pending, one rejected, one suspended to match the mobile demo-accounts requirement), service categories matching the 9 listed in the mobile context, a spread of bookings across every status, some reviews, complaints, welfare programmes and earnings. Field values must be plausible enough to demo (e.g. worker locations genuinely near each other for geo-matching to look sensible).
```
**Commit:** `feat(db): add initial Alembic migration and seed script with demo data`

---

### Prompt 5 — Geo-query helpers
```
Add backend/app/db/geo_queries.py (or similar) with reusable PostGIS query helpers: nearby_workers(lat, lng, radius_km, skill=None, limit=None) ordered by distance using ST_DWithin/ST_Distance on the geography column, with a proper spatial index (GiST) on Worker.location. Write a quick standalone test/check confirming distance ordering is correct against a few seeded points. These helpers are what Yash's workers/bookings endpoints and Yash-Thakur's matching service will both call — do not duplicate this logic elsewhere.
```
**Commit:** `feat(db): add PostGIS geo-query helpers for nearby-worker lookups with spatial index`

---

### Prompt 6 — Constraints, indexes and enum documentation
```
Review all models from Prompts 2-3 and add missing NOT NULL constraints, unique constraints (e.g. one review per booking), and indexes on frequently-filtered/sorted columns (booking.status, booking.type, worker.verificationStatus, worker.availability, createdAt columns used for sorting). Generate the follow-up Alembic migration. Then write docs/api/DB_SCHEMA.md: one table per entity listing every column, type, constraint and enum values, matching the mobile entity table 1:1 so any teammate can cross-check without opening the code.
```
**Commit:** `chore(db): add missing constraints/indexes and document full schema in DB_SCHEMA.md`

---

### Prompt 7 — Sync pass with mobile mock data
```
Open mobile/src/mock/data/ (once Janhvi/Priti/Ashana have added mock data files) and diff every entity's field names/shapes against your schema and docs/api/DB_SCHEMA.md. List every mismatch in docs/api/MOBILE_API_REQUESTS.md under a "Schema mismatches found" section (don't unilaterally rename either side — flag it for a quick sync). This prompt should be re-run whenever a mobile teammate adds a new mock data file.
```
**Commit:** `docs(db): reconcile schema field names against mobile mock data, log mismatches`