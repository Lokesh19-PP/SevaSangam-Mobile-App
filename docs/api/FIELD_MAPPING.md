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

---

## ServiceCategory

| Mobile (camelCase) | DB Column (snake_case) | Type | Notes |
| --- | --- | --- | --- |
| `id` | `id` | UUID | PK |
| `key` | `key` | String(50) | Unique |
| `name` | `name` | String(100) | i18n key |
| `icon` | `icon` | String(100) | |
| `baseVisitCharge` | `base_visit_charge` | Float | ₹ |

## Booking

| Mobile (camelCase) | DB Column (snake_case) | Type | Notes |
| --- | --- | --- | --- |
| `id` | `id` | UUID | PK |
| `customerId` | `customer_id` | UUID FK → `users.id` | RESTRICT |
| `workerId` | `worker_id` | UUID FK → `workers.id` | SET NULL (allows unassigned) |
| `serviceId` | `service_id` | UUID FK → `service_categories.id` | RESTRICT |
| `type` | `type` | Enum(`booking_type`) | `scheduled` / `emergency` |
| `status` | `status` | Enum(`booking_status`) | `pending`→`assigned`→`accepted`→`en_route`→`in_progress`→`completed`, + `rejected`/`cancelled`/`unassigned` |
| `scheduledAt` | `scheduled_at` | DateTime(tz) | |
| `address.text` | `address_text` | String(500) | |
| `address.lat` | `address_lat` | Float | |
| `address.lng` | `address_lng` | Float | |
| `notes` | `notes` | Text | |
| `priceEstimate` | `price_estimate` | Float | |
| `paymentMode` | `payment_mode` | String(20) | |
| `paymentStatus` | `payment_status` | Enum(`payment_status`) | `pending` / `paid` / `cash` |
| `matchReason` | `match_reason` | String(500) | AI explanation |
| `timeline` | `timeline` | JSONB | Array of `{status, timestamp, note}` |

## Review

| Mobile (camelCase) | DB Column (snake_case) | Type | Notes |
| --- | --- | --- | --- |
| `id` | `id` | UUID | PK |
| `bookingId` | `booking_id` | UUID FK → `bookings.id` | CASCADE, unique (1 review per booking) |
| `customerId` | `customer_id` | UUID FK → `users.id` | RESTRICT |
| `workerId` | `worker_id` | UUID FK → `workers.id` | RESTRICT |
| `stars` | `stars` | Integer | CHECK 1–5 |
| `comment` | `comment` | Text | |
| `tags` | `tags` | ARRAY(String) | |

## Complaint

| Mobile (camelCase) | DB Column (snake_case) | Type | Notes |
| --- | --- | --- | --- |
| `id` | `id` | UUID | PK |
| `raisedBy` | `raised_by` | UUID FK → `users.id` | SET NULL (audit trail) |
| `bookingId` | `booking_id` | UUID FK → `bookings.id` | SET NULL, nullable |
| `workerId` | `worker_id` | UUID FK → `workers.id` | SET NULL, nullable |
| `category` | `category` | String(100) | |
| `description` | `description` | Text | |
| `status` | `status` | Enum(`complaint_status`) | `open` / `in_review` / `resolved` / `rejected` |
| `resolutionNote` | `resolution_note` | Text | |

## WelfareProgram

| Mobile (camelCase) | DB Column (snake_case) | Type | Notes |
| --- | --- | --- | --- |
| `id` | `id` | UUID | PK |
| `title` | `title` | String(255) | |
| `description` | `description` | Text | |
| `type` | `type` | Enum(`welfare_program_type`) | `insurance` / `health` / `training` / `other` |
| `eligibility` | `eligibility` | String(500) | |
| `enrolledCount` | `enrolled_count` | Integer | |
| `status` | `status` | Enum(`welfare_program_status`) | `active` / `draft` / `closed` |

## Earning

| Mobile (camelCase) | DB Column (snake_case) | Type | Notes |
| --- | --- | --- | --- |
| `id` | `id` | UUID | PK |
| `workerId` | `worker_id` | UUID FK → `workers.id` | RESTRICT |
| `bookingId` | `booking_id` | UUID FK → `bookings.id` | RESTRICT |
| `amount` | `amount` | Float | ₹ |
| `paymentStatus` | `payment_status` | Enum(`payment_status`) | `pending` / `paid` / `cash` |
| `date` | `date` | Date | |

## Notification

| Mobile (camelCase) | DB Column (snake_case) | Type | Notes |
| --- | --- | --- | --- |
| `id` | `id` | UUID | PK |
| `userId` | `user_id` | UUID FK → `users.id` | CASCADE |
| `type` | `type` | String(50) | |
| `titleKey` | `title_key` | String(100) | i18n key |
| `body` | `body` | Text | |
| `read` | `read` | Boolean | Default `false` |

---

## Foreign Key Cascade Policy

| FK column | Parent table | On Delete | Rationale |
| --- | --- | --- | --- |
| `workers.user_id` | `users` | **CASCADE** | Worker profile is an extension of User |
| `workers.cooperative_id` | `cooperatives` | **SET NULL** | Worker survives without a cooperative |
| `certificates.worker_id` | `workers` | **CASCADE** | Certificates belong to the worker |
| `bookings.customer_id` | `users` | **RESTRICT** | Cannot delete a user who has bookings |
| `bookings.worker_id` | `workers` | **SET NULL** | Allows unassigned emergency bookings |
| `bookings.service_id` | `service_categories` | **RESTRICT** | Cannot delete a service with bookings |
| `reviews.booking_id` | `bookings` | **CASCADE** | Review is tied to its booking |
| `reviews.customer_id` | `users` | **RESTRICT** | Cannot delete user who left reviews |
| `reviews.worker_id` | `workers` | **RESTRICT** | Cannot delete worker who has reviews |
| `complaints.raised_by` | `users` | **SET NULL** | Complaint survives as audit trail |
| `complaints.booking_id` | `bookings` | **SET NULL** | Complaint survives if booking removed |
| `complaints.worker_id` | `workers` | **SET NULL** | Complaint survives if worker removed |
| `earnings.worker_id` | `workers` | **RESTRICT** | Cannot delete worker with earnings |
| `earnings.booking_id` | `bookings` | **RESTRICT** | Cannot delete booking with earnings |
| `notifications.user_id` | `users` | **CASCADE** | Notifications deleted with user |

### Policy summary

- **RESTRICT** = business-critical data (bookings, earnings, reviews) — you cannot delete the parent without first handling the children.
- **CASCADE** = ownership data (worker profile, certificates, notifications) — deleting the parent takes the children with it.
- **SET NULL** = audit/reference data (complaints, unassigned bookings) — the record survives with a null reference.
