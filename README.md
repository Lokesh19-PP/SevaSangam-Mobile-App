# 🤝 SevaSangam — Labour Cooperative Digital Service Marketplace

[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16.0-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![PostGIS](https://img.shields.io/badge/PostGIS-3.4-336791?logo=postgresql&logoColor=white)](https://postgis.net/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red?logo=python&logoColor=white)](https://www.sqlalchemy.org/)
[![Alembic](https://img.shields.io/badge/Alembic-Migrations-orange)](https://alembic.sqlalchemy.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)

**SevaSangam** is a cooperative-owned digital service marketplace developed for **Smart India Hackathon (SIH 2026, Problem Statement 26089 — Ministry of Cooperation / NCCT)**. It connects customers directly with verified, skilled workers from Labour Cooperative Societies — electricians, plumbers, carpenters, domestic help, caregivers, drivers, gardeners, cleaners, and technicians.

This repository contains the **PostgreSQL + PostGIS database infrastructure, SQLAlchemy models, Pydantic schemas, spatial geo-query engine, database migrations, and seed automation** supporting both the mobile application and backend services.

---

## 🏛️ System Architecture & Tech Stack

- **Database**: PostgreSQL 16 + PostGIS 3.4 (`postgis/postgis:16-3.4` container)
- **ORM & Geometry**: SQLAlchemy 2.0 + GeoAlchemy2 (WGS 84 SRID 4326 Geography Points)
- **Data Validation**: Pydantic v2
- **Database Migrations**: Alembic
- **Spatial Indexing**: GiST index (`idx_workers_location`) for ultra-fast `ST_DWithin` & `ST_Distance` geo-queries
- **Containerization**: Docker Compose

---

## 📋 Entity & Database Schema (11 Core Entities)

The database schema is mapped 1:1 with the mobile application context doc (`docs/ANTIGRAVITY_MOBILE_CONTEXT.md` § 7):

| # | Entity | Table Name | Key Description |
|---|---|---|---|
| 1 | **User** | `users` | Customer, Worker, and Admin profiles with phone & language preferences |
| 2 | **Cooperative** | `cooperatives` | Labour Cooperative Societies managing worker groups across regions |
| 3 | **Worker** | `workers` | Worker profiles, PostGIS location point, skills array, ratings, insurance & availability |
| 4 | **Certificate** | `certificates` | Licenses, trade certs, OCR confidence metadata & verification notes |
| 5 | **ServiceCategory** | `service_categories` | 9 default categories (electrician, plumber, carpenter, caregiver, driver, etc.) |
| 6 | **Booking** | `bookings` | Scheduled & Emergency SOS bookings across 9 statuses with JSONB timeline logs |
| 7 | **Review** | `reviews` | Customer 1-5 star ratings, comments, and tag labels (1 review per booking constraint) |
| 8 | **Complaint** | `complaints` | Dispute management for overcharging, unavailability, or quality issues |
| 9 | **WelfareProgram** | `welfare_programs` | Micro-insurance, health cover & skill training schemes for co-op workers |
| 10 | **Earning** | `earnings` | Financial earning records linked to bookings for payout tracking |
| 11 | **Notification** | `notifications` | In-app push notifications for booking updates, SOS alerts & verification status |

---

## 🚀 Quick Start Guide

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Python 3.12+](https://www.python.org/)

### 1. Environment Configuration
Copy the sample environment file into `backend/`:
```bash
cp backend/.env.example backend/.env
```

### 2. Start PostgreSQL + PostGIS Container
Navigate to `docker/` and launch the database service:
```bash
cd docker
docker compose up -d
```
*The database will run on `localhost:5433` (Database: `sevasangam`, User: `sevasangam`).*

### 3. Run Alembic Database Migrations
From the repository root, install requirements and apply database migrations:
```bash
pip install -r backend/requirements.txt
python -m alembic upgrade head
```

### 4. Seed Database with Realistic Demo Data
Populate 21 users, 15 workers with PostGIS coordinates in Pune/Mumbai, demo account states (`pending`, `rejected`, `suspended`, `verified`), 9 service categories, and bookings across all 9 statuses:
```bash
python -m backend.scripts.seed_db
```

### 5. Run PostGIS Spatial Query Verification Tests
Verify PostGIS distance calculations, GiST spatial indexing, distance ordering, and skill/availability filtering:
```bash
python -m backend.tests.test_geo_queries
```

---

## 📍 PostGIS Geo-Query Helpers

The platform uses PostGIS geography calculations for worker matching and nearby worker discovery. The reusable helper module is located at [`backend/app/db/geo_queries.py`](file:///c:/Users/lokes/OneDrive/Desktop/GIT-REPO/SIH-2026%28APP%29/SevaSangam-Mobile-App/backend/app/db/geo_queries.py):

```python
from backend.app.db.geo_queries import nearby_workers, nearby_workers_async

# Find verified electricians within 10km of Pune center sorted strictly by distance
results = nearby_workers(
    db=session,
    lat=18.5204,
    lng=73.8567,
    radius_km=10.0,
    skill="electrician",
    limit=5
)

for worker, distance_km in results:
    print(f"Worker {worker.id} is {distance_km:.2f} km away")
```

---

## 📚 Documentation Reference Index

Detailed technical documentation is available in the [`docs/`](file:///c:/Users/lokes/OneDrive/Desktop/GIT-REPO/SIH-2026%28APP%29/SevaSangam-Mobile-App/docs/) directory:

- 📖 **[DB Setup Guide](docs/api/DB_SETUP.md)** — Docker setup, connection strings & PostGIS extension check.
- 📐 **[Full Database Schema Spec](docs/api/DB_SCHEMA.md)** — Complete 1:1 table columns, data types, indexes & constraints reference.
- 🔄 **[Field Mapping Reference](docs/api/FIELD_MAPPING.md)** — Mapping table from mobile `camelCase` to DB `snake_case`.
- 📝 **[Mobile API & Mismatch Log](docs/api/MOBILE_API_REQUESTS.md)** — Tracking frontend mock data reconciliation.
- 🎯 **[Mobile Context Specification](docs/ANTIGRAVITY_MOBILE_CONTEXT.md)** — Overall project domain rules & mobile requirements.

---

## 📜 License & Acknowledgments

Developed for **SIH 2026 (Problem Statement 26089)** under the **Ministry of Cooperation / National Council for Cooperative Training (NCCT)**.