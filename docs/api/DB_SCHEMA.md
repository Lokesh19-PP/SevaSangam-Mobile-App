# SevaSangam Database Schema Documentation

This document provides a 1:1 mapping and comprehensive reference of the PostgreSQL + PostGIS database schema for the SevaSangam platform. It matches the entity definitions in the mobile context (`docs/ANTIGRAVITY_MOBILE_CONTEXT.md` § 7) and backend SQLAlchemy models.

---

## 1. Enum Definitions

| Enum Name | Postgres Native Type | Allowed Values | Usage |
|---|---|---|---|
| `user_role` | `user_role` | `'customer'`, `'worker'`, `'admin'` | `users.role` |
| `verification_status` | `verification_status` | `'pending'`, `'verified'`, `'rejected'`, `'suspended'` | `workers.verification_status` |
| `worker_availability` | `worker_availability` | `'available'`, `'busy'`, `'offline'` | `workers.availability` |
| `insurance_status` | `insurance_status` | `'active'`, `'expired'`, `'none'` | `workers.insurance_status` |
| `certificate_status` | `certificate_status` | `'pending'`, `'approved'`, `'rejected'` | `certificates.status` |
| `booking_type` | `booking_type` | `'scheduled'`, `'emergency'` | `bookings.type` |
| `booking_status` | `booking_status` | `'pending'`, `'assigned'`, `'accepted'`, `'en_route'`, `'in_progress'`, `'completed'`, `'rejected'`, `'cancelled'`, `'unassigned'` | `bookings.status` |
| `payment_status` | `payment_status` | `'pending'`, `'paid'`, `'cash'` | `bookings.payment_status`, `earnings.payment_status` |
| `complaint_status` | `complaint_status` | `'open'`, `'in_review'`, `'resolved'`, `'rejected'` | `complaints.status` |
| `welfare_program_type` | `welfare_program_type` | `'insurance'`, `'health'`, `'training'`, `'other'` | `welfare_programs.type` |
| `welfare_program_status` | `welfare_program_status` | `'active'`, `'draft'`, `'closed'` | `welfare_programs.status` |

---

## 2. Entity Tables

### 2.1 `users`
Stores user profile information for customers, workers, and admins.

| Mobile Field | DB Column | Type | Constraints | Default | Description |
|---|---|---|---|---|---|
| `id` | `id` | `UUID` | **PK**, NOT NULL | `uuid4()` | Unique User ID |
| `role` | `role` | `user_role` | Enum, NOT NULL, **INDEX** | — | User role (`customer`/`worker`/`admin`) |
| `name` | `name` | `VARCHAR(255)` | NOT NULL | — | Full name |
| `phone` | `phone` | `VARCHAR(15)` | **UNIQUE**, NOT NULL | — | Phone (+91 Indian format) |
| `language` | `language` | `VARCHAR(5)` | NOT NULL | `'en'` | Preferred language code (`en`, `hi`, `mr`) |
| `avatar` | `avatar` | `VARCHAR(512)` | Nullable | `NULL` | Profile avatar URL |
| `createdAt` | `created_at` | `TIMESTAMPTZ` | NOT NULL, **INDEX** | `now()` | Timestamp created |
| `updatedAt` | `updated_at` | `TIMESTAMPTZ` | NOT NULL | `now()` | Timestamp last updated |

---

### 2.2 `cooperatives`
Stores Labour Cooperative Societies managing worker groups.

| Mobile Field | DB Column | Type | Constraints | Default | Description |
|---|---|---|---|---|---|
| `id` | `id` | `UUID` | **PK**, NOT NULL | `uuid4()` | Unique Cooperative ID |
| `name` | `name` | `VARCHAR(255)` | NOT NULL | — | Name of society |
| `region` | `region` | `VARCHAR(255)` | NOT NULL, **INDEX** | — | Operating region / district |
| `memberCount` | `member_count` | `INTEGER` | NOT NULL | `0` | Active member count |
| `verified` | `verified` | `BOOLEAN` | NOT NULL, **INDEX** | `false` | Society verification status |
| `createdAt` | `created_at` | `TIMESTAMPTZ` | NOT NULL, **INDEX** | `now()` | Timestamp created |
| `updatedAt` | `updated_at` | `TIMESTAMPTZ` | NOT NULL | `now()` | Timestamp updated |

---

### 2.3 `workers`
Stores worker professional details, PostGIS geolocation, skills, and insurance information.

| Mobile Field | DB Column | Type | Constraints | Default | Description |
|---|---|---|---|---|---|
| `id` | `id` | `UUID` | **PK**, NOT NULL | `uuid4()` | Unique Worker ID |
| `userId` | `user_id` | `UUID` | **FK** (`users.id` CASCADE), **UNIQUE**, NOT NULL | — | Linked User account |
| `cooperativeId` | `cooperative_id` | `UUID` | **FK** (`cooperatives.id` SET NULL), Nullable, **INDEX** | `NULL` | Linked Labour Cooperative |
| `skills[]` | `skills` | `VARCHAR[]` | NOT NULL | `{}` | Array of skill keys |
| `experienceYears` | `experience_years` | `INTEGER` | NOT NULL | `0` | Years of experience |
| `rating` | `rating` | `FLOAT` | NOT NULL, **INDEX** | `0.0` | Average star rating (0-5) |
| `ratingCount` | `rating_count` | `INTEGER` | NOT NULL | `0` | Total review count |
| `verificationStatus` | `verification_status` | `verification_status` | Enum, NOT NULL, **INDEX** | `'pending'` | Verification state |
| `availability` | `availability` | `worker_availability` | Enum, NOT NULL, **INDEX** | `'offline'` | Current availability |
| `location{lat,lng}` | `location` | `geography(POINT, 4326)` | **GiST INDEX** (`idx_workers_location`), Nullable | `NULL` | PostGIS spatial point |
| `serviceRadiusKm` | `service_radius_km` | `FLOAT` | NOT NULL | `10.0` | Max operational distance in km |
| `workloadThisWeek` | `workload_this_week` | `INTEGER` | NOT NULL | `0` | Active bookings completed/assigned this week |
| `insurance.status` | `insurance_status` | `insurance_status` | Enum, NOT NULL | `'none'` | Worker micro-insurance status |
| `insurance.coverage` | `insurance_coverage` | `VARCHAR(255)` | Nullable | `NULL` | Coverage details description |
| `insurance.validTill` | `insurance_valid_till` | `DATE` | Nullable | `NULL` | Expiry date of policy |
| `createdAt` | `created_at` | `TIMESTAMPTZ` | NOT NULL, **INDEX** | `now()` | Timestamp created |
| `updatedAt` | `updated_at` | `TIMESTAMPTZ` | NOT NULL | `now()` | Timestamp updated |

---

### 2.4 `certificates`
Stores trade licenses, safety certificates, and OCR verification metadata.

| Mobile Field | DB Column | Type | Constraints | Default | Description |
|---|---|---|---|---|---|
| `id` | `id` | `UUID` | **PK**, NOT NULL | `uuid4()` | Unique Certificate ID |
| `workerId` | `worker_id` | `UUID` | **FK** (`workers.id` CASCADE), NOT NULL, **INDEX** | — | Owning worker |
| `type` | `type` | `VARCHAR(100)` | NOT NULL | — | Cert type (e.g. `electrician_license`) |
| `imageUrl` | `image_url` | `VARCHAR(512)` | Nullable | `NULL` | Document photo URL |
| `ocr.text` | `ocr_text` | `TEXT` | Nullable | `NULL` | Extracted OCR text |
| `ocr.confidence` | `ocr_confidence` | `FLOAT` | Nullable | `NULL` | OCR confidence score (0.0-1.0) |
| `status` | `status` | `certificate_status` | Enum, NOT NULL, **INDEX** | `'pending'` | Review status |
| `reviewNote` | `review_note` | `TEXT` | Nullable | `NULL` | Admin review notes |
| `createdAt` | `created_at` | `TIMESTAMPTZ` | NOT NULL, **INDEX** | `now()` | Timestamp created |
| `updatedAt` | `updated_at` | `TIMESTAMPTZ` | NOT NULL | `now()` | Timestamp updated |

---

### 2.5 `service_categories`
Stores available service types on the platform (9 default categories).

| Mobile Field | DB Column | Type | Constraints | Default | Description |
|---|---|---|---|---|---|
| `id` | `id` | `UUID` | **PK**, NOT NULL | `uuid4()` | Unique Service Category ID |
| `key` | `key` | `VARCHAR(50)` | **UNIQUE**, NOT NULL | — | Service key (e.g., `electrician`) |
| `name` | `name` | `VARCHAR(100)` | NOT NULL | — | i18n label key (e.g., `services.electrician`) |
| `icon` | `icon` | `VARCHAR(100)` | Nullable | `NULL` | Icon identifier/URL |
| `baseVisitCharge` | `base_visit_charge` | `FLOAT` | NOT NULL | `0.0` | Base visitation fee (₹) |
| `createdAt` | `created_at` | `TIMESTAMPTZ` | NOT NULL, **INDEX** | `now()` | Timestamp created |
| `updatedAt` | `updated_at` | `TIMESTAMPTZ` | NOT NULL | `now()` | Timestamp updated |

---

### 2.6 `bookings`
Stores scheduled and emergency service bookings between customers and workers.

| Mobile Field | DB Column | Type | Constraints | Default | Description |
|---|---|---|---|---|---|
| `id` | `id` | `UUID` | **PK**, NOT NULL | `uuid4()` | Unique Booking ID |
| `customerId` | `customer_id` | `UUID` | **FK** (`users.id` RESTRICT), NOT NULL, **INDEX** | — | Booking customer |
| `workerId` | `worker_id` | `UUID` | **FK** (`workers.id` SET NULL), Nullable, **INDEX** | `NULL` | Assigned worker (NULL if unassigned) |
| `serviceId` | `service_id` | `UUID` | **FK** (`service_categories.id` RESTRICT), NOT NULL, **INDEX** | — | Service category |
| `type` | `type` | `booking_type` | Enum, NOT NULL, **INDEX** | — | Booking type (`scheduled`/`emergency`) |
| `status` | `status` | `booking_status` | Enum, NOT NULL, **INDEX** | `'pending'` | Lifecycle state |
| `scheduledAt` | `scheduled_at` | `TIMESTAMPTZ` | Nullable, **INDEX** | `NULL` | Scheduled appointment time |
| `address.text` | `address_text` | `VARCHAR(500)` | Nullable | `NULL` | Human readable address |
| `address.lat` | `address_lat` | `FLOAT` | Nullable | `NULL` | Customer latitude |
| `address.lng` | `address_lng` | `FLOAT` | Nullable | `NULL` | Customer longitude |
| `notes` | `notes` | `TEXT` | Nullable | `NULL` | Special work instructions |
| `priceEstimate` | `price_estimate` | `FLOAT` | Nullable | `NULL` | Calculated price estimate (₹) |
| `paymentMode` | `payment_mode` | `VARCHAR(20)` | Nullable | `NULL` | Payment method (`cash`, `online`) |
| `paymentStatus` | `payment_status` | `payment_status` | Enum, NOT NULL | `'pending'` | Payment status |
| `matchReason` | `match_reason` | `VARCHAR(500)` | Nullable | `NULL` | AI auto-match explanation |
| `timeline[]` | `timeline` | `JSONB` | NOT NULL | `[]` | Status history audit log |
| `createdAt` | `created_at` | `TIMESTAMPTZ` | NOT NULL, **INDEX** | `now()` | Timestamp created |
| `updatedAt` | `updated_at` | `TIMESTAMPTZ` | NOT NULL | `now()` | Timestamp updated |

---

### 2.7 `reviews`
Stores customer ratings, feedback, and tags for completed bookings.

| Mobile Field | DB Column | Type | Constraints | Default | Description |
|---|---|---|---|---|---|
| `id` | `id` | `UUID` | **PK**, NOT NULL | `uuid4()` | Unique Review ID |
| `bookingId` | `booking_id` | `UUID` | **FK** (`bookings.id` CASCADE), **UNIQUE**, NOT NULL | — | Associated booking (1 review per booking) |
| `customerId` | `customer_id` | `UUID` | **FK** (`users.id` RESTRICT), NOT NULL, **INDEX** | — | Customer leaving review |
| `workerId` | `worker_id` | `UUID` | **FK** (`workers.id` RESTRICT), NOT NULL, **INDEX** | — | Worker receiving review |
| `stars` | `stars` | `INTEGER` | NOT NULL, **CHECK** (`stars >= 1 AND stars <= 5`) | — | Rating score (1 to 5) |
| `comment` | `comment` | `TEXT` | Nullable | `NULL` | Review text |
| `tags[]` | `tags` | `VARCHAR[]` | NOT NULL | `{}` | Feedback tag labels (e.g. `["punctual", "expert"]`) |
| `createdAt` | `created_at` | `TIMESTAMPTZ` | NOT NULL, **INDEX** | `now()` | Timestamp created |
| `updatedAt` | `updated_at` | `TIMESTAMPTZ` | NOT NULL | `now()` | Timestamp updated |

---

### 2.8 `complaints`
Stores complaints raised by users against workers or booking issues.

| Mobile Field | DB Column | Type | Constraints | Default | Description |
|---|---|---|---|---|---|
| `id` | `id` | `UUID` | **PK**, NOT NULL | `uuid4()` | Unique Complaint ID |
| `raisedBy` | `raised_by` | `UUID` | **FK** (`users.id` SET NULL), Nullable, **INDEX** | `NULL` | Complainant user ID |
| `bookingId` | `booking_id` | `UUID` | **FK** (`bookings.id` SET NULL), Nullable, **INDEX** | `NULL` | Optional linked booking ID |
| `workerId` | `worker_id` | `UUID` | **FK** (`workers.id` SET NULL), Nullable, **INDEX** | `NULL` | Optional linked worker ID |
| `category` | `category` | `VARCHAR(100)` | NOT NULL | — | Category (e.g. `Overcharging`) |
| `description` | `description` | `TEXT` | NOT NULL | — | Complaint details |
| `status` | `status` | `complaint_status` | Enum, NOT NULL, **INDEX** | `'open'` | Resolution lifecycle state |
| `resolutionNote` | `resolution_note` | `TEXT` | Nullable | `NULL` | Admin resolution notes |
| `createdAt` | `created_at` | `TIMESTAMPTZ` | NOT NULL, **INDEX** | `now()` | Timestamp created |
| `updatedAt` | `updated_at` | `TIMESTAMPTZ` | NOT NULL | `now()` | Timestamp updated |

---

### 2.9 `welfare_programs`
Stores government and cooperative welfare, insurance, and skill training programs.

| Mobile Field | DB Column | Type | Constraints | Default | Description |
|---|---|---|---|---|---|
| `id` | `id` | `UUID` | **PK**, NOT NULL | `uuid4()` | Unique Program ID |
| `title` | `title` | `VARCHAR(255)` | NOT NULL | — | Program title |
| `description` | `description` | `TEXT` | Nullable | `NULL` | Detailed description |
| `type` | `type` | `welfare_program_type` | Enum, NOT NULL, **INDEX** | — | Program type (`insurance`/`health`/`training`) |
| `eligibility` | `eligibility` | `VARCHAR(500)` | Nullable | `NULL` | Eligibility criteria text |
| `enrolledCount` | `enrolled_count` | `INTEGER` | NOT NULL | `0` | Total enrolled workers |
| `status` | `status` | `welfare_program_status` | Enum, NOT NULL, **INDEX** | `'draft'` | Availability status |
| `createdAt` | `created_at` | `TIMESTAMPTZ` | NOT NULL, **INDEX** | `now()` | Timestamp created |
| `updatedAt` | `updated_at` | `TIMESTAMPTZ` | NOT NULL | `now()` | Timestamp updated |

---

### 2.10 `earnings`
Stores financial earnings history per booking for workers.

| Mobile Field | DB Column | Type | Constraints | Default | Description |
|---|---|---|---|---|---|
| `id` | `id` | `UUID` | **PK**, NOT NULL | `uuid4()` | Unique Earning Record ID |
| `workerId` | `worker_id` | `UUID` | **FK** (`workers.id` RESTRICT), NOT NULL, **INDEX** | — | Worker earning money |
| `bookingId` | `booking_id` | `UUID` | **FK** (`bookings.id` RESTRICT), NOT NULL, **INDEX** | — | Linked booking |
| `amount` | `amount` | `FLOAT` | NOT NULL | — | Earning amount (₹) |
| `paymentStatus` | `payment_status` | `payment_status` | Enum, NOT NULL, **INDEX** | `'pending'` | Payout status |
| `date` | `date` | `DATE` | NOT NULL, **INDEX** | — | Earning date |
| `createdAt` | `created_at` | `TIMESTAMPTZ` | NOT NULL, **INDEX** | `now()` | Timestamp created |
| `updatedAt` | `updated_at` | `TIMESTAMPTZ` | NOT NULL | `now()` | Timestamp updated |

---

### 2.11 `notifications`
Stores push/in-app notifications sent to platform users.

| Mobile Field | DB Column | Type | Constraints | Default | Description |
|---|---|---|---|---|---|
| `id` | `id` | `UUID` | **PK**, NOT NULL | `uuid4()` | Unique Notification ID |
| `userId` | `user_id` | `UUID` | **FK** (`users.id` CASCADE), NOT NULL, **INDEX** | — | Target recipient user ID |
| `type` | `type` | `VARCHAR(50)` | NOT NULL | — | Category (e.g. `booking_update`, `sos_alert`) |
| `titleKey` | `title_key` | `VARCHAR(100)` | NOT NULL | — | i18n title label key |
| `body` | `body` | `TEXT` | Nullable | `NULL` | Notification body message |
| `read` | `read` | `BOOLEAN` | NOT NULL, **INDEX** | `false` | Read flag status |
| `createdAt` | `created_at` | `TIMESTAMPTZ` | NOT NULL, **INDEX** | `now()` | Timestamp created |
| `updatedAt` | `updated_at` | `TIMESTAMPTZ` | NOT NULL | `now()` | Timestamp updated |

---

## 3. Foreign Key & Cascade Policy Summary

- **`users` deletion**: Cascades to `workers` and `notifications`. Customer reference in `bookings`, `reviews` blocked via `RESTRICT`.
- **`cooperatives` deletion**: Nullifies `workers.cooperative_id` (`SET NULL`).
- **`workers` deletion**: Cascades to `certificates`. References in `bookings`, `complaints` set to `SET NULL`. References in `reviews`, `earnings` blocked via `RESTRICT`.
- **`bookings` deletion**: Cascades to `reviews`. Set to `SET NULL` on `complaints`. References in `earnings` blocked via `RESTRICT`.
