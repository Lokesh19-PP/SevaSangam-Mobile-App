# Mobile API Requests & Schema Reconciliation Log

This document logs schema reconciliation passes, field mapping diffs, and schema mismatches between the mobile frontend mock data (`mobile/src/mock/data/`) and the PostgreSQL database schema ([`docs/api/DB_SCHEMA.md`](file:///c:/Users/lokes/OneDrive/Desktop/GIT-REPO/SIH-2026%28APP%29/SevaSangam-Mobile-App/docs/api/DB_SCHEMA.md)).

---

## Status of `mobile/src/mock/data/`

* **Last Checked**: 2026-09-23
* **Directory Status**: `mobile/src/mock/data/` does not exist yet (mobile teammates Janhvi / Priti / Ashana have not yet created/pushed the mobile mock files).
* **Baseline Verification**: The DB schema was verified 1:1 against `docs/ANTIGRAVITY_MOBILE_CONTEXT.md` § 7.

---

## Schema Mismatches Found

> *Note: This section is updated whenever a mobile teammate adds or modifies mock data files in `mobile/src/mock/data/`.*

### Current Audit Log:
- **Status**: No mock data files present in `mobile/src/mock/data/` at this time.
- **Baseline Alignment**:
  - All 11 entities (`User`, `Cooperative`, `Worker`, `Certificate`, `ServiceCategory`, `Booking`, `Review`, `Complaint`, `WelfareProgram`, `Earning`, `Notification`) in [`docs/api/DB_SCHEMA.md`](file:///c:/Users/lokes/OneDrive/Desktop/GIT-REPO/SIH-2026%28APP%29/SevaSangam-Mobile-App/docs/api/DB_SCHEMA.md) match the entity table in `docs/ANTIGRAVITY_MOBILE_CONTEXT.md` § 7 1:1.
  - camelCase mobile field names are mapped to snake_case DB columns systematically as documented in [`docs/api/FIELD_MAPPING.md`](file:///c:/Users/lokes/OneDrive/Desktop/GIT-REPO/SIH-2026%28APP%29/SevaSangam-Mobile-App/docs/api/FIELD_MAPPING.md).

---

## Instructions for Re-running Prompt 7

Whenever Janhvi, Priti, or Ashana add mock data files to `mobile/src/mock/data/`:
1. Inspect the JSON / JS exports in `mobile/src/mock/data/*.js`.
2. Compare each entity's keys and nested structures against `docs/api/DB_SCHEMA.md` and `docs/api/FIELD_MAPPING.md`.
3. Log any newly discovered mismatches under "Schema mismatches found" above without renaming fields on either side.
