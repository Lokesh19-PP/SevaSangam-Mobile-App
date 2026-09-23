"""
PostGIS Geo-Query Helpers.

Reusable PostGIS spatial query helpers for nearby-worker lookups.
Ordered by distance using ST_DWithin and ST_Distance on the geography column,
utilizing the GiST spatial index `idx_workers_location` on Worker.location.

Used by Yash's workers/bookings endpoints and Yash-Thakur's matching service.
"""

from typing import List, Tuple, Optional
from sqlalchemy import select, and_
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from geoalchemy2.functions import ST_DWithin, ST_Distance, ST_SetSRID, ST_MakePoint

from backend.app.models.worker import Worker
from backend.app.models.enums import VerificationStatus, WorkerAvailability


def build_nearby_workers_query(
    lat: float,
    lng: float,
    radius_km: float = 10.0,
    skill: Optional[str] = None,
    verification_status: Optional[VerificationStatus] = VerificationStatus.VERIFIED,
    availability: Optional[WorkerAvailability] = None,
    limit: Optional[int] = None,
):
    """
    Builds a SQLAlchemy select statement for nearby workers sorted by distance.

    Returns a tuple of (Worker model, distance_km).
    Uses ST_DWithin on PostGIS geography column (leverages GiST spatial index idx_workers_location).
    """
    # Create reference geography point (SRID 4326: WGS84 lat/lng). Note: ST_MakePoint(lng, lat)
    ref_point = ST_SetSRID(ST_MakePoint(lng, lat), 4326)

    # Convert radius from km to meters (PostGIS geography unit = meters)
    radius_meters = radius_km * 1000.0

    distance_meters_expr = ST_Distance(Worker.location, ref_point)
    distance_km_expr = (distance_meters_expr / 1000.0).label("distance_km")

    conditions = [
        Worker.location.isnot(None),
        ST_DWithin(Worker.location, ref_point, radius_meters),
    ]

    if verification_status is not None:
        conditions.append(Worker.verification_status == verification_status)

    if availability is not None:
        conditions.append(Worker.availability == availability)

    if skill is not None:
        # Check if skill exists in worker's PostgreSQL skills array
        conditions.append(Worker.skills.any(skill))

    stmt = (
        select(Worker, distance_km_expr)
        .where(and_(*conditions))
        .order_by(distance_km_expr.asc())
    )

    if limit is not None and limit > 0:
        stmt = stmt.limit(limit)

    return stmt


def nearby_workers(
    db: Session,
    lat: float,
    lng: float,
    radius_km: float = 10.0,
    skill: Optional[str] = None,
    limit: Optional[int] = None,
    verification_status: Optional[VerificationStatus] = VerificationStatus.VERIFIED,
    availability: Optional[WorkerAvailability] = None,
) -> List[Tuple[Worker, float]]:
    """
    Synchronous helper to retrieve nearby workers sorted by distance.

    Returns a list of tuples: [(Worker, distance_km), ...]
    """
    stmt = build_nearby_workers_query(
        lat=lat,
        lng=lng,
        radius_km=radius_km,
        skill=skill,
        verification_status=verification_status,
        availability=availability,
        limit=limit,
    )
    result = db.execute(stmt).all()
    return [(row[0], float(row[1])) for row in result]


async def nearby_workers_async(
    db: AsyncSession,
    lat: float,
    lng: float,
    radius_km: float = 10.0,
    skill: Optional[str] = None,
    limit: Optional[int] = None,
    verification_status: Optional[VerificationStatus] = VerificationStatus.VERIFIED,
    availability: Optional[WorkerAvailability] = None,
) -> List[Tuple[Worker, float]]:
    """
    Asynchronous helper to retrieve nearby workers sorted by distance.

    Returns a list of tuples: [(Worker, distance_km), ...]
    """
    stmt = build_nearby_workers_query(
        lat=lat,
        lng=lng,
        radius_km=radius_km,
        skill=skill,
        verification_status=verification_status,
        availability=availability,
        limit=limit,
    )
    result = await db.execute(stmt)
    rows = result.all()
    return [(row[0], float(row[1])) for row in rows]
