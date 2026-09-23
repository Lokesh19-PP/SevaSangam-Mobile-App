# Mobile ↔ Database Field Name Mapping

> Auto-generated for Prompt 2. Keep updated as models evolve.
> **Convention:** mobile uses `camelCase`, database uses `snake_case`.

## User

| Mobile (camelCase) | DB Column (snake_case) | Type | Notes |
| --- | --- | --- | --- |
| `id` | `id` | UUID | PK |
| `role` | `role` | Enum(`user_role`) | `customer` / `worker` / `admin` |
| `name` | `name` | String(255) | |
| `phone` | `phone` | String(15) | Unique, +91 format |
| `language` | `language` | String(5) | `en` / `hi` / `mr` |
| `avatar` | `avatar` | String(512) | URL, nullable |

## Cooperative

| Mobile (camelCase) | DB Column (snake_case) | Type | Notes |
| --- | --- | --- | --- |
| `id` | `id` | UUID | PK |
| `name` | `name` | String(255) | |
| `region` | `region` | String(255) | |
| `memberCount` | `member_count` | Integer | |
| `verified` | `verified` | Boolean | |

## Worker

| Mobile (camelCase) | DB Column (snake_case) | Type | Notes |
| --- | --- | --- | --- |
| `id` | `id` | UUID | PK |
| `userId` | `user_id` | UUID FK → `users.id` | CASCADE delete |
| `cooperativeId` | `cooperative_id` | UUID FK → `cooperatives.id` | SET NULL on delete |
| `skills` | `skills` | ARRAY(String) | |
| `experienceYears` | `experience_years` | Integer | |
| `rating` | `rating` | Float | |
| `ratingCount` | `rating_count` | Integer | |
| `verificationStatus` | `verification_status` | Enum(`verification_status`) | `pending` / `verified` / `rejected` / `suspended` |
| `availability` | `availability` | Enum(`worker_availability`) | `available` / `busy` / `offline` |
| `location.lat` / `location.lng` | `location` | Geography(POINT, 4326) | Stored as `POINT(lng lat)` — note order |
| `serviceRadiusKm` | `service_radius_km` | Float | |
| `workloadThisWeek` | `workload_this_week` | Integer | |
| `insurance.status` | `insurance_status` | Enum(`insurance_status`) | `active` / `expired` / `none` |
| `insurance.coverage` | `insurance_coverage` | String(255) | |
| `insurance.validTill` | `insurance_valid_till` | Date | |

## Certificate

| Mobile (camelCase) | DB Column (snake_case) | Type | Notes |
| --- | --- | --- | --- |
| `id` | `id` | UUID | PK |
| `workerId` | `worker_id` | UUID FK → `workers.id` | CASCADE delete |
| `type` | `type` | String(100) | e.g. `electrician_license` |
| `imageUrl` | `image_url` | String(512) | |
| `ocr.text` | `ocr_text` | Text | |
| `ocr.confidence` | `ocr_confidence` | Float | |
| `status` | `status` | Enum(`certificate_status`) | `pending` / `approved` / `rejected` |
| `reviewNote` | `review_note` | Text | |

## Nested → Flat mapping summary

The mobile API uses nested objects for some fields. The database stores them as flat columns:

| Mobile shape | DB columns |
| --- | --- |
| `location: { lat, lng }` | `location` (PostGIS Geography POINT) |
| `insurance: { status, coverage, validTill }` | `insurance_status`, `insurance_coverage`, `insurance_valid_till` |
| `ocr: { text, confidence }` | `ocr_text`, `ocr_confidence` |

Pydantic response schemas re-nest these back to match the mobile contract.
