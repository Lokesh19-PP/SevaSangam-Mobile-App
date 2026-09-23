"""
Database Seed Script for SevaSangam.

Populates realistic demo data into Postgres+PostGIS DB:
- 3 Cooperatives
- 9 Service Categories (matching mobile context)
- 21 Users (5 Customers, 1 Admin, 15 Workers)
- 15 Workers across skills, locations (Pune/Mumbai), availability & verification states (including pending, rejected, suspended)
- Certificates (approved, pending, rejected)
- Bookings across all 9 statuses (pending, assigned, accepted, en_route, in_progress, completed, rejected, cancelled, unassigned)
- Reviews, Complaints, Welfare Programs, Earnings, and Notifications.

Run via:
    python -m backend.scripts.seed_db
or
    python backend/scripts/seed_db.py
"""

import sys
import os
from datetime import datetime, timedelta, date

# Ensure root workspace is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from geoalchemy2.elements import WKTElement
from sqlalchemy.orm import Session

from backend.app.db.session import sync_engine, SyncSessionLocal
from backend.app.models.user import User
from backend.app.models.cooperative import Cooperative
from backend.app.models.worker import Worker
from backend.app.models.certificate import Certificate
from backend.app.models.service_category import ServiceCategory
from backend.app.models.booking import Booking
from backend.app.models.review import Review
from backend.app.models.complaint import Complaint
from backend.app.models.welfare_program import WelfareProgram
from backend.app.models.earning import Earning
from backend.app.models.notification import Notification

from backend.app.models.enums import (
    UserRole,
    VerificationStatus,
    WorkerAvailability,
    InsuranceStatus,
    CertificateStatus,
    BookingStatus,
    BookingType,
    PaymentStatus,
    ComplaintStatus,
    WelfareProgramType,
    WelfareProgramStatus,
)


def seed():
    session = SyncSessionLocal()

    try:
        print("Cleaning old data...")
        session.query(Notification).delete()
        session.query(Earning).delete()
        session.query(Complaint).delete()
        session.query(Review).delete()
        session.query(Booking).delete()
        session.query(Certificate).delete()
        session.query(Worker).delete()
        session.query(User).delete()
        session.query(Cooperative).delete()
        session.query(ServiceCategory).delete()
        session.query(WelfareProgram).delete()
        session.commit()

        print("Seeding Service Categories...")
        categories = [
            ServiceCategory(key="electrician", name="services.electrician", icon="flash-outline", base_visit_charge=250.0),
            ServiceCategory(key="plumber", name="services.plumber", icon="water-outline", base_visit_charge=200.0),
            ServiceCategory(key="carpenter", name="services.carpenter", icon="hammer-outline", base_visit_charge=300.0),
            ServiceCategory(key="domestic_help", name="services.domestic_help", icon="home-outline", base_visit_charge=150.0),
            ServiceCategory(key="caregiver", name="services.caregiver", icon="heart-outline", base_visit_charge=350.0),
            ServiceCategory(key="driver", name="services.driver", icon="car-outline", base_visit_charge=200.0),
            ServiceCategory(key="gardener", name="services.gardener", icon="flower-outline", base_visit_charge=180.0),
            ServiceCategory(key="cleaner", name="services.cleaner", icon="sparkles-outline", base_visit_charge=150.0),
            ServiceCategory(key="technician", name="services.technician", icon="build-outline", base_visit_charge=250.0),
        ]
        session.add_all(categories)
        session.commit()
        cat_map = {c.key: c for c in categories}

        print("Seeding Cooperatives...")
        coop_pune = Cooperative(name="Pune Shramik Labour Co-op Society", region="Pune", member_count=45, verified=True)
        coop_mumbai = Cooperative(name="Mumbai Central Shramik Union", region="Mumbai", member_count=120, verified=True)
        coop_nashik = Cooperative(name="Nashik Kaushalya Cooperative", region="Nashik", member_count=15, verified=False)
        session.add_all([coop_pune, coop_mumbai, coop_nashik])
        session.commit()

        print("Seeding Customers & Admin...")
        c1 = User(name="Aarav Sharma", phone="+919876543210", role=UserRole.CUSTOMER, language="en")
        c2 = User(name="Priya Patel", phone="+919876543211", role=UserRole.CUSTOMER, language="hi")
        c3 = User(name="Rohan Verma", phone="+919876543212", role=UserRole.CUSTOMER, language="mr")
        c4 = User(name="Ananya Deshmukh", phone="+919876543213", role=UserRole.CUSTOMER, language="mr")
        c5 = User(name="Vikram Singh", phone="+919876543214", role=UserRole.CUSTOMER, language="en")
        admin = User(name="System Admin", phone="+919000000000", role=UserRole.ADMIN, language="en")
        session.add_all([c1, c2, c3, c4, c5, admin])
        session.commit()

        print("Seeding Workers & Worker Users...")
        # 15 Workers: W1..W12 verified, W13 pending, W14 rejected, W15 suspended
        worker_data = [
            # Verified workers in Pune (lat ~18.52, lng ~73.85)
            {"name": "Ramesh Kumar", "phone": "+919123456701", "skills": ["electrician", "plumber"], "exp": 7, "rating": 4.8, "rcount": 42, "status": VerificationStatus.VERIFIED, "avail": WorkerAvailability.AVAILABLE, "lat": 18.5204, "lng": 73.8567, "coop": coop_pune, "ins": InsuranceStatus.ACTIVE, "cov": "₹2,00,000 Health & Accident", "workload": 4},
            {"name": "Suresh Shinde", "phone": "+919123456702", "skills": ["plumber", "cleaner"], "exp": 5, "rating": 4.5, "rcount": 18, "status": VerificationStatus.VERIFIED, "avail": WorkerAvailability.BUSY, "lat": 18.5250, "lng": 73.8500, "coop": coop_pune, "ins": InsuranceStatus.ACTIVE, "cov": "₹1,50,000 General Protection", "workload": 8},
            {"name": "Rajesh Patil", "phone": "+919123456703", "skills": ["carpenter"], "exp": 10, "rating": 4.9, "rcount": 56, "status": VerificationStatus.VERIFIED, "avail": WorkerAvailability.AVAILABLE, "lat": 18.5180, "lng": 73.8600, "coop": coop_pune, "ins": InsuranceStatus.ACTIVE, "cov": "₹3,00,000 Comprehensive", "workload": 2},
            {"name": "Sunita Gaikwad", "phone": "+919123456704", "skills": ["domestic_help", "caregiver"], "exp": 4, "rating": 4.7, "rcount": 31, "status": VerificationStatus.VERIFIED, "avail": WorkerAvailability.AVAILABLE, "lat": 18.5300, "lng": 73.8400, "coop": coop_pune, "ins": InsuranceStatus.EXPIRED, "cov": None, "workload": 5},
            {"name": "Ganesh Jadhav", "phone": "+919123456705", "skills": ["electrician", "technician"], "exp": 6, "rating": 4.6, "rcount": 24, "status": VerificationStatus.VERIFIED, "avail": WorkerAvailability.AVAILABLE, "lat": 18.5150, "lng": 73.8520, "coop": coop_pune, "ins": InsuranceStatus.ACTIVE, "cov": "₹2,00,000 Standard Shield", "workload": 3},
            {"name": "Laxmi Pawar", "phone": "+919123456706", "skills": ["caregiver"], "exp": 8, "rating": 4.9, "rcount": 60, "status": VerificationStatus.VERIFIED, "avail": WorkerAvailability.BUSY, "lat": 18.5220, "lng": 73.8650, "coop": coop_pune, "ins": InsuranceStatus.ACTIVE, "cov": "₹2,50,000 Health Cover", "workload": 7},
            {"name": "Anil Kadam", "phone": "+919123456707", "skills": ["driver"], "exp": 12, "rating": 4.3, "rcount": 15, "status": VerificationStatus.VERIFIED, "avail": WorkerAvailability.AVAILABLE, "lat": 18.5100, "lng": 73.8450, "coop": coop_pune, "ins": InsuranceStatus.ACTIVE, "cov": "₹1,00,000 Vehicle & Driver Shield", "workload": 1},
            {"name": "Manoj Bhosale", "phone": "+919123456708", "skills": ["gardener"], "exp": 3, "rating": 4.4, "rcount": 12, "status": VerificationStatus.VERIFIED, "avail": WorkerAvailability.OFFLINE, "lat": 18.5350, "lng": 73.8700, "coop": coop_pune, "ins": InsuranceStatus.NONE, "cov": None, "workload": 0},
            {"name": "Deepak More", "phone": "+919123456709", "skills": ["cleaner"], "exp": 2, "rating": 4.2, "rcount": 9, "status": VerificationStatus.VERIFIED, "avail": WorkerAvailability.AVAILABLE, "lat": 18.5050, "lng": 73.8550, "coop": coop_pune, "ins": InsuranceStatus.ACTIVE, "cov": "₹1,00,000 Basic Cover", "workload": 2},
            {"name": "Nitin Thorat", "phone": "+919123456710", "skills": ["technician"], "exp": 9, "rating": 4.8, "rcount": 38, "status": VerificationStatus.VERIFIED, "avail": WorkerAvailability.AVAILABLE, "lat": 18.5280, "lng": 73.8620, "coop": coop_pune, "ins": InsuranceStatus.ACTIVE, "cov": "₹2,00,000 Tech Shield", "workload": 4},

            # Verified workers in Mumbai (lat ~19.07, lng ~72.87)
            {"name": "Vijay Chavan", "phone": "+919123456711", "skills": ["electrician"], "exp": 5, "rating": 4.1, "rcount": 5, "status": VerificationStatus.VERIFIED, "avail": WorkerAvailability.OFFLINE, "lat": 19.0760, "lng": 72.8777, "coop": coop_mumbai, "ins": InsuranceStatus.ACTIVE, "cov": "₹2,00,000 Mumbai Co-op Shield", "workload": 0},
            {"name": "Sangita Mane", "phone": "+919123456712", "skills": ["domestic_help"], "exp": 6, "rating": 4.6, "rcount": 20, "status": VerificationStatus.VERIFIED, "avail": WorkerAvailability.AVAILABLE, "lat": 19.0800, "lng": 72.8800, "coop": coop_mumbai, "ins": InsuranceStatus.ACTIVE, "cov": "₹1,50,000 Health Cover", "workload": 3},

            # Demo accounts: Pending, Rejected, Suspended
            {"name": "Rahul Kamble (Pending)", "phone": "+919123456713", "skills": ["electrician"], "exp": 2, "rating": 0.0, "rcount": 0, "status": VerificationStatus.PENDING, "avail": WorkerAvailability.OFFLINE, "lat": 18.5190, "lng": 73.8580, "coop": coop_pune, "ins": InsuranceStatus.NONE, "cov": None, "workload": 0},
            {"name": "Prakash Salunkhe (Rejected)", "phone": "+919123456714", "skills": ["plumber"], "exp": 1, "rating": 0.0, "rcount": 0, "status": VerificationStatus.REJECTED, "avail": WorkerAvailability.OFFLINE, "lat": 18.5210, "lng": 73.8510, "coop": coop_nashik, "ins": InsuranceStatus.NONE, "cov": None, "workload": 0},
            {"name": "Mahesh Sawant (Suspended)", "phone": "+919123456715", "skills": ["carpenter"], "exp": 4, "rating": 2.5, "rcount": 8, "status": VerificationStatus.SUSPENDED, "avail": WorkerAvailability.OFFLINE, "lat": 18.5170, "lng": 73.8540, "coop": coop_pune, "ins": InsuranceStatus.EXPIRED, "cov": None, "workload": 0},
        ]

        created_workers = []
        for wd in worker_data:
            user = User(name=wd["name"], phone=wd["phone"], role=UserRole.WORKER, language="mr" if "Pawar" in wd["name"] or "Patil" in wd["name"] else "en")
            session.add(user)
            session.flush()

            # Point geometry: POINT(lng lat) Note: Longitude first in WKT
            point_wkt = f"POINT({wd['lng']} {wd['lat']})"
            worker = Worker(
                user_id=user.id,
                cooperative_id=wd["coop"].id if wd["coop"] else None,
                skills=wd["skills"],
                experience_years=wd["exp"],
                rating=wd["rating"],
                rating_count=wd["rcount"],
                verification_status=wd["status"],
                availability=wd["avail"],
                location=WKTElement(point_wkt, srid=4326),
                service_radius_km=10.0,
                workload_this_week=wd["workload"],
                insurance_status=wd["ins"],
                insurance_coverage=wd["cov"],
                insurance_valid_till=date.today() + timedelta(days=180) if wd["ins"] == InsuranceStatus.ACTIVE else None,
            )
            session.add(worker)
            created_workers.append(worker)

        session.commit()

        print("Seeding Certificates...")
        # Approved certs for Ramesh, Suresh, Rajesh
        cert1 = Certificate(worker_id=created_workers[0].id, type="electrician_license", image_url="https://example.com/certs/elec1.jpg", ocr_text="Govt Electrical License #MH-EL-9082", ocr_confidence=0.96, status=CertificateStatus.APPROVED, review_note="Verified by Co-op Admin")
        cert2 = Certificate(worker_id=created_workers[1].id, type="plumbing_cert", image_url="https://example.com/certs/plumb1.jpg", ocr_text="National Skill Development Cert - Plumbing Grade A", ocr_confidence=0.92, status=CertificateStatus.APPROVED, review_note="Verified by Co-op Admin")
        cert3 = Certificate(worker_id=created_workers[2].id, type="carpentry_cert", image_url="https://example.com/certs/carp1.jpg", ocr_text="ITI Carpentry Master Certificate", ocr_confidence=0.98, status=CertificateStatus.APPROVED, review_note="Verified by Co-op Admin")

        # Pending cert for Rahul (Pending worker)
        cert_pending = Certificate(worker_id=created_workers[12].id, type="electrician_license", image_url="https://example.com/certs/elec_pending.jpg", ocr_text="Apprentice License #MH-AP-1029", ocr_confidence=0.88, status=CertificateStatus.PENDING, review_note=None)

        # Rejected cert for Prakash (Rejected worker)
        cert_rejected = Certificate(worker_id=created_workers[13].id, type="plumbing_cert", image_url="https://example.com/certs/plumb_rej.jpg", ocr_text="Unreadable Document", ocr_confidence=0.41, status=CertificateStatus.REJECTED, review_note="OCR failure: Document blurred and missing seal.")

        session.add_all([cert1, cert2, cert3, cert_pending, cert_rejected])
        session.commit()

        print("Seeding Bookings across ALL 9 statuses...")
        now = datetime.utcnow()
        w_ramesh = created_workers[0]
        w_suresh = created_workers[1]
        w_rajesh = created_workers[2]
        w_sunita = created_workers[3]

        bookings = [
            # 1. PENDING (scheduled, assigned to worker)
            Booking(
                customer_id=c1.id,
                worker_id=w_ramesh.id,
                service_id=cat_map["electrician"].id,
                type=BookingType.SCHEDULED,
                status=BookingStatus.PENDING,
                scheduled_at=now + timedelta(hours=5),
                address_text="Flat 402, Sunshine Apartments, FC Road, Pune",
                address_lat=18.5200,
                address_lng=73.8560,
                notes="Fix flickering lights in living room",
                price_estimate=450.0,
                payment_mode="online",
                payment_status=PaymentStatus.PENDING,
                match_reason="Matched by distance (0.8km) and rating (4.8)",
                timeline=[{"status": "pending", "timestamp": now.isoformat(), "note": "Booking created"}]
            ),
            # 2. ASSIGNED
            Booking(
                customer_id=c2.id,
                worker_id=w_suresh.id,
                service_id=cat_map["plumber"].id,
                type=BookingType.SCHEDULED,
                status=BookingStatus.ASSIGNED,
                scheduled_at=now + timedelta(hours=2),
                address_text="House 12, Swargate, Pune",
                address_lat=18.5020,
                address_lng=73.8580,
                notes="Bathroom pipe leakage",
                price_estimate=350.0,
                payment_mode="cash",
                payment_status=PaymentStatus.PENDING,
                match_reason="Cooperative dispatch auto-assigned",
                timeline=[
                    {"status": "pending", "timestamp": (now - timedelta(minutes=30)).isoformat(), "note": "Booking created"},
                    {"status": "assigned", "timestamp": (now - timedelta(minutes=15)).isoformat(), "note": "Assigned to Suresh Shinde"}
                ]
            ),
            # 3. ACCEPTED
            Booking(
                customer_id=c3.id,
                worker_id=w_rajesh.id,
                service_id=cat_map["carpenter"].id,
                type=BookingType.SCHEDULED,
                status=BookingStatus.ACCEPTED,
                scheduled_at=now + timedelta(hours=1),
                address_text="Plot 88, Kothrud, Pune",
                address_lat=18.5074,
                address_lng=73.8077,
                notes="Repair main door latch",
                price_estimate=500.0,
                payment_mode="online",
                payment_status=PaymentStatus.PENDING,
                match_reason="Direct booking by customer",
                timeline=[
                    {"status": "pending", "timestamp": (now - timedelta(hours=1)).isoformat(), "note": "Booking created"},
                    {"status": "assigned", "timestamp": (now - timedelta(minutes=50)).isoformat(), "note": "Assigned to Rajesh"},
                    {"status": "accepted", "timestamp": (now - timedelta(minutes=40)).isoformat(), "note": "Worker accepted booking"}
                ]
            ),
            # 4. EN_ROUTE
            Booking(
                customer_id=c4.id,
                worker_id=w_sunita.id,
                service_id=cat_map["caregiver"].id,
                type=BookingType.SCHEDULED,
                status=BookingStatus.EN_ROUTE,
                scheduled_at=now + timedelta(minutes=15),
                address_text="Bungalow 5, Aundh, Pune",
                address_lat=18.5600,
                address_lng=73.8070,
                notes="Elderly assistance for 4 hours",
                price_estimate=800.0,
                payment_mode="online",
                payment_status=PaymentStatus.PAID,
                match_reason="Specialized skill match & top rated caregiver",
                timeline=[
                    {"status": "accepted", "timestamp": (now - timedelta(minutes=30)).isoformat(), "note": "Accepted"},
                    {"status": "en_route", "timestamp": (now - timedelta(minutes=10)).isoformat(), "note": "Worker started journey"}
                ]
            ),
            # 5. IN_PROGRESS
            Booking(
                customer_id=c1.id,
                worker_id=w_ramesh.id,
                service_id=cat_map["electrician"].id,
                type=BookingType.EMERGENCY,
                status=BookingStatus.IN_PROGRESS,
                scheduled_at=now - timedelta(minutes=20),
                address_text="Shop 14, MG Road, Camp, Pune",
                address_lat=18.5180,
                address_lng=73.8750,
                notes="Emergency circuit breaker trip",
                price_estimate=600.0,
                payment_mode="cash",
                payment_status=PaymentStatus.PENDING,
                match_reason="SOS Emergency match (<1km)",
                timeline=[
                    {"status": "accepted", "timestamp": (now - timedelta(minutes=25)).isoformat(), "note": "SOS Accepted"},
                    {"status": "in_progress", "timestamp": (now - timedelta(minutes=10)).isoformat(), "note": "Work started"}
                ]
            ),
            # 6. COMPLETED
            Booking(
                customer_id=c5.id,
                worker_id=w_ramesh.id,
                service_id=cat_map["electrician"].id,
                type=BookingType.SCHEDULED,
                status=BookingStatus.COMPLETED,
                scheduled_at=now - timedelta(days=1),
                address_text="Villa 9, Baner, Pune",
                address_lat=18.5590,
                address_lng=73.7868,
                notes="Full ceiling fan installation",
                price_estimate=750.0,
                payment_mode="online",
                payment_status=PaymentStatus.PAID,
                match_reason="Preferred customer request",
                timeline=[
                    {"status": "completed", "timestamp": (now - timedelta(hours=20)).isoformat(), "note": "Job finished successfully"}
                ]
            ),
            # 7. REJECTED (by worker)
            Booking(
                customer_id=c2.id,
                worker_id=w_suresh.id,
                service_id=cat_map["plumber"].id,
                type=BookingType.SCHEDULED,
                status=BookingStatus.REJECTED,
                scheduled_at=now - timedelta(hours=3),
                address_text="Flat 101, Deccan, Pune",
                address_lat=18.5160,
                address_lng=73.8400,
                notes="Drainage cleaning",
                price_estimate=300.0,
                payment_mode="cash",
                payment_status=PaymentStatus.PENDING,
                match_reason="Auto-matched",
                timeline=[
                    {"status": "rejected", "timestamp": (now - timedelta(hours=2)).isoformat(), "note": "Worker unavailable at requested time"}
                ]
            ),
            # 8. CANCELLED (by customer)
            Booking(
                customer_id=c3.id,
                worker_id=w_rajesh.id,
                service_id=cat_map["carpenter"].id,
                type=BookingType.SCHEDULED,
                status=BookingStatus.CANCELLED,
                scheduled_at=now - timedelta(hours=6),
                address_text="Viman Nagar, Pune",
                address_lat=18.5679,
                address_lng=73.9143,
                notes="Furniture assembly",
                price_estimate=1200.0,
                payment_mode="online",
                payment_status=PaymentStatus.PENDING,
                match_reason="Direct booking",
                timeline=[
                    {"status": "cancelled", "timestamp": (now - timedelta(hours=5)).isoformat(), "note": "Customer cancelled due to plan change"}
                ]
            ),
            # 9. UNASSIGNED (emergency booking with no taker yet)
            Booking(
                customer_id=c4.id,
                worker_id=None,
                service_id=cat_map["technician"].id,
                type=BookingType.EMERGENCY,
                status=BookingStatus.UNASSIGNED,
                scheduled_at=now,
                address_text="Shivajinagar Bus Stand, Pune",
                address_lat=18.5314,
                address_lng=73.8446,
                notes="Generator control board fault — URGENT!",
                price_estimate=900.0,
                payment_mode="online",
                payment_status=PaymentStatus.PENDING,
                match_reason="Broadcasting to all nearby technicians within 10km",
                timeline=[
                    {"status": "unassigned", "timestamp": now.isoformat(), "note": "Emergency broadcast active"}
                ]
            )
        ]
        session.add_all(bookings)
        session.commit()

        print("Seeding Reviews...")
        rev1 = Review(
            booking_id=bookings[5].id,  # COMPLETED booking
            customer_id=c5.id,
            worker_id=w_ramesh.id,
            stars=5,
            comment="Ramesh was extremely prompt and professional. Installed all 3 ceiling fans without any mess!",
            tags=["punctual", "polite", "expert", "clean_work"]
        )
        session.add(rev1)
        session.commit()

        print("Seeding Complaints...")
        comp1 = Complaint(
            raised_by=c2.id,
            booking_id=bookings[6].id,  # REJECTED booking
            worker_id=w_suresh.id,
            category="Worker Unavailability",
            description="Worker rejected the booking without contacting me, despite showing available status in app.",
            status=ComplaintStatus.IN_REVIEW,
            resolution_note="Support team reviewing worker availability toggle logs."
        )
        comp2 = Complaint(
            raised_by=c3.id,
            booking_id=None,
            worker_id=created_workers[14].id,  # Suspended worker
            category="Overcharging Complaint",
            description="Worker requested extra cash over the estimated rate.",
            status=ComplaintStatus.RESOLVED,
            resolution_note="Worker suspended pending cooperative committee review."
        )
        session.add_all([comp1, comp2])
        session.commit()

        print("Seeding Welfare Programs...")
        welfare1 = WelfareProgram(
            title="Ayushman Bharat Co-op Health Cover",
            description="Comprehensive health insurance covering hospitalization up to ₹5 Lakhs for verified co-op workers.",
            type=WelfareProgramType.HEALTH,
            eligibility="Verified active workers with >6 months co-op membership",
            enrolled_count=38,
            status=WelfareProgramStatus.ACTIVE
        )
        welfare2 = WelfareProgram(
            title="Worker Safety & Electrical Certification 2026",
            description="Free 3-day advanced electrical safety & solar panel installation training module.",
            type=WelfareProgramType.TRAINING,
            eligibility="Electricians with verified license",
            enrolled_count=15,
            status=WelfareProgramStatus.ACTIVE
        )
        welfare3 = WelfareProgram(
            title="Laborer Accident Insurance Suraksha",
            description="Personal accident cover up to ₹2 Lakhs with instant claim dispatch via cooperative union.",
            type=WelfareProgramType.INSURANCE,
            eligibility="All registered workers",
            enrolled_count=92,
            status=WelfareProgramStatus.ACTIVE
        )
        session.add_all([welfare1, welfare2, welfare3])
        session.commit()

        print("Seeding Earnings...")
        earning1 = Earning(
            worker_id=w_ramesh.id,
            booking_id=bookings[5].id,  # COMPLETED booking
            amount=750.0,
            payment_status=PaymentStatus.PAID,
            date=date.today() - timedelta(days=1)
        )
        session.add(earning1)
        session.commit()

        print("Seeding Notifications...")
        n1 = Notification(
            user_id=c1.id,
            type="booking_update",
            title_key="notifications.booking_started",
            body="Ramesh Kumar has started work on your Emergency booking.",
            read=False
        )
        n2 = Notification(
            user_id=w_ramesh.user_id,
            type="emergency",
            title_key="notifications.sos_alert",
            body="New emergency booking nearby in Camp, Pune!",
            read=True
        )
        n3 = Notification(
            user_id=created_workers[12].user_id,  # Pending worker
            type="verification",
            title_key="notifications.verification_pending",
            body="Your electrical certificate is under review by Pune Shramik Co-op admin.",
            read=False
        )
        session.add_all([n1, n2, n3])
        session.commit()

        print("Seed completed successfully!")

    except Exception as e:
        session.rollback()
        print(f"Error during seed: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    seed()
