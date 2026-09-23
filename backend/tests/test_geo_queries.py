"""
Standalone test check for PostGIS geo-query helpers.

Tests distance calculation, strict ascending ordering, skill filtering,
limit filtering, and status filtering against the seeded database.
"""

import sys
import os

# Ensure root workspace is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.app.db.session import SyncSessionLocal
from backend.app.db.geo_queries import nearby_workers
from backend.app.models.enums import VerificationStatus, WorkerAvailability


def test_geo_queries():
    session = SyncSessionLocal()
    try:
        print("--- Test 1: Nearby workers within 10km of Pune Center (18.5204, 73.8567) ---")
        pune_lat, pune_lng = 18.5204, 73.8567
        results = nearby_workers(session, lat=pune_lat, lng=pune_lng, radius_km=10.0)

        print(f"Found {len(results)} verified workers within 10km:")
        assert len(results) > 0, "Should find workers near Pune center"

        prev_distance = -1.0
        for idx, (worker, dist_km) in enumerate(results, 1):
            print(f"  {idx}. Worker ID: {worker.id} | User ID: {worker.user_id} | Skills: {worker.skills} | Distance: {dist_km:.3f} km | Status: {worker.verification_status.value}")
            # Assert distance is strictly increasing (ordered by distance ASC)
            assert dist_km >= prev_distance, f"Distance ordering failed at index {idx}: {dist_km} < {prev_distance}"
            # Assert within 10km radius
            assert dist_km <= 10.0, f"Worker {worker.id} at {dist_km}km exceeded 10km radius"
            # Assert only verified workers returned by default
            assert worker.verification_status == VerificationStatus.VERIFIED
            prev_distance = dist_km

        print("[PASS] Test 1 PASSED: Strict distance ordering & radius filtering verified.\n")

        print("--- Test 2: Filter by Skill ('electrician') ---")
        elec_results = nearby_workers(session, lat=pune_lat, lng=pune_lng, radius_km=10.0, skill="electrician")
        print(f"Found {len(elec_results)} electricians:")
        for worker, dist_km in elec_results:
            print(f"  - Worker ID: {worker.id} | Skills: {worker.skills} | Distance: {dist_km:.3f} km")
            assert "electrician" in worker.skills, f"Worker {worker.id} does not have electrician skill"

        print("[PASS] Test 2 PASSED: Skill filtering verified.\n")

        print("--- Test 3: Filter by Limit (limit=2) ---")
        limit_results = nearby_workers(session, lat=pune_lat, lng=pune_lng, radius_km=10.0, limit=2)
        print(f"Found {len(limit_results)} workers with limit=2:")
        assert len(limit_results) <= 2, "Limit filtering failed"
        print("[PASS] Test 3 PASSED: Limit constraint verified.\n")

        print("--- Test 4: Filter by Availability ('available') ---")
        avail_results = nearby_workers(
            session,
            lat=pune_lat,
            lng=pune_lng,
            radius_km=10.0,
            availability=WorkerAvailability.AVAILABLE
        )
        print(f"Found {len(avail_results)} available workers:")
        for worker, dist_km in avail_results:
            assert worker.availability == WorkerAvailability.AVAILABLE
            print(f"  - Worker ID: {worker.id} | Avail: {worker.availability.value} | Distance: {dist_km:.3f} km")

        print("[PASS] Test 4 PASSED: Availability filtering verified.\n")

        print("--- Test 5: Verify Excluded Unverified/Pending Workers ---")
        all_nearby_incl_unverified = nearby_workers(
            session,
            lat=pune_lat,
            lng=pune_lng,
            radius_km=10.0,
            verification_status=None
        )
        unverified_ids = [w.id for w, _ in all_nearby_incl_unverified if w.verification_status != VerificationStatus.VERIFIED]
        default_ids = [w.id for w, _ in results]
        for u_id in unverified_ids:
            assert u_id not in default_ids, f"Unverified worker {u_id} should not be in default verified results"

        print("[PASS] Test 5 PASSED: Verification status exclusion verified.\n")

        print("=== ALL GEO-QUERY TESTS PASSED SUCCESSFULLY ===")

    finally:
        session.close()


if __name__ == "__main__":
    test_geo_queries()
