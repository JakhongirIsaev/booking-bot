"""
Booking Service — create, list, and cancel bookings.

Handles the full booking lifecycle:
- Creating new bookings (with slot validation)
- Listing client's bookings
- Cancelling bookings
- Admin queries (today's bookings, upcoming, stats)
"""

import uuid
from datetime import date, datetime, time, timedelta
from typing import List, Optional
from zoneinfo import ZoneInfo

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.config.settings import settings
from app.models.booking import Booking, BookingStatus
from app.models.service import Service
from app.services.schedule_service import get_available_slots


async def create_booking(
    session: AsyncSession,
    business_id: uuid.UUID,
    client_id: uuid.UUID,
    staff_id: uuid.UUID,
    service_id: uuid.UUID,
    start_time: datetime,
) -> Booking | None:
    """
    Create a new booking after validating the time slot is available.

    Steps:
    1. Get service duration to calculate end_time
    2. Check for conflicting bookings
    3. Create and save the booking

    Returns:
        Booking object if successful, None if slot is already taken
    """
    # Get service for duration
    service_result = await session.execute(
        select(Service).where(Service.id == service_id)
    )
    service = service_result.scalar_one_or_none()
    if service is None:
        return None

    end_time = start_time + timedelta(minutes=service.duration_minutes)

    # Double-check for conflicts (race condition protection)
    conflict_result = await session.execute(
        select(Booking).where(
            and_(
                Booking.staff_id == staff_id,
                Booking.status.in_([BookingStatus.PENDING, BookingStatus.CONFIRMED]),
                Booking.start_time < end_time,
                Booking.end_time > start_time,
            )
        )
    )

    if conflict_result.scalar_one_or_none() is not None:
        return None  # Slot is already taken

    # Create booking
    booking = Booking(
        business_id=business_id,
        client_id=client_id,
        staff_id=staff_id,
        service_id=service_id,
        start_time=start_time,
        end_time=end_time,
        status=BookingStatus.CONFIRMED,
    )
    session.add(booking)
    await session.flush()

    return booking


async def get_client_bookings(
    session: AsyncSession,
    client_id: uuid.UUID,
) -> List[Booking]:
    """
    Get all upcoming bookings for a client.

    Returns bookings sorted by start_time ascending.
    Only shows confirmed/pending bookings that haven't passed yet.
    """
    tz = ZoneInfo(settings.timezone)
    now = datetime.now(tz)

    result = await session.execute(
        select(Booking)
        .options(
            selectinload(Booking.service),
            selectinload(Booking.staff),
        )
        .where(
            and_(
                Booking.client_id == client_id,
                Booking.status.in_([BookingStatus.PENDING, BookingStatus.CONFIRMED]),
                Booking.start_time >= now,
            )
        )
        .order_by(Booking.start_time.asc())
    )
    return list(result.scalars().all())


async def cancel_booking(
    session: AsyncSession,
    booking_id: uuid.UUID,
    client_id: uuid.UUID,
) -> bool:
    """
    Cancel a booking. Only the owning client can cancel.

    Returns True if cancelled, False if booking not found or unauthorized.
    """
    result = await session.execute(
        select(Booking).where(
            and_(
                Booking.id == booking_id,
                Booking.client_id == client_id,
                Booking.status.in_([BookingStatus.PENDING, BookingStatus.CONFIRMED]),
            )
        )
    )
    booking = result.scalar_one_or_none()

    if booking is None:
        return False

    booking.status = BookingStatus.CANCELLED
    await session.flush()
    return True


async def get_bookings_for_date(
    session: AsyncSession,
    business_id: uuid.UUID,
    target_date: date,
) -> List[Booking]:
    """
    Get all bookings for a business on a specific date.
    Used by admin to view the schedule.
    """
    tz = ZoneInfo(settings.timezone)
    day_start = datetime.combine(target_date, time.min, tzinfo=tz)
    day_end = datetime.combine(target_date, time.max, tzinfo=tz)

    result = await session.execute(
        select(Booking)
        .options(
            selectinload(Booking.service),
            selectinload(Booking.staff),
            selectinload(Booking.client),
        )
        .where(
            and_(
                Booking.business_id == business_id,
                Booking.start_time >= day_start,
                Booking.end_time <= day_end,
                Booking.status.in_([BookingStatus.PENDING, BookingStatus.CONFIRMED]),
            )
        )
        .order_by(Booking.start_time.asc())
    )
    return list(result.scalars().all())


async def get_all_upcoming_bookings(
    session: AsyncSession,
    business_id: uuid.UUID,
    limit: int = 20,
) -> List[Booking]:
    """Get all upcoming bookings for a business (admin view)."""
    tz = ZoneInfo(settings.timezone)
    now = datetime.now(tz)

    result = await session.execute(
        select(Booking)
        .options(
            selectinload(Booking.service),
            selectinload(Booking.staff),
            selectinload(Booking.client),
        )
        .where(
            and_(
                Booking.business_id == business_id,
                Booking.start_time >= now,
                Booking.status.in_([BookingStatus.PENDING, BookingStatus.CONFIRMED]),
            )
        )
        .order_by(Booking.start_time.asc())
        .limit(limit)
    )
    return list(result.scalars().all())


async def get_booking_stats(
    session: AsyncSession,
    business_id: uuid.UUID,
) -> dict:
    """
    Get basic booking statistics for admin dashboard.

    Returns:
        dict with total_bookings, today_bookings, total_clients
    """
    tz = ZoneInfo(settings.timezone)
    now = datetime.now(tz)
    today_start = datetime.combine(now.date(), time.min, tzinfo=tz)
    today_end = datetime.combine(now.date(), time.max, tzinfo=tz)

    # Total bookings
    total_result = await session.execute(
        select(func.count(Booking.id)).where(
            Booking.business_id == business_id
        )
    )
    total_bookings = total_result.scalar() or 0

    # Today's bookings
    today_result = await session.execute(
        select(func.count(Booking.id)).where(
            and_(
                Booking.business_id == business_id,
                Booking.start_time >= today_start,
                Booking.end_time <= today_end,
                Booking.status.in_([BookingStatus.PENDING, BookingStatus.CONFIRMED]),
            )
        )
    )
    today_bookings = today_result.scalar() or 0

    # Unique clients
    clients_result = await session.execute(
        select(func.count(func.distinct(Booking.client_id))).where(
            Booking.business_id == business_id
        )
    )
    total_clients = clients_result.scalar() or 0

    return {
        "total_bookings": total_bookings,
        "today_bookings": today_bookings,
        "total_clients": total_clients,
    }
