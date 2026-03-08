"""
Schedule Service — time slot generation.

This is the CORE ALGORITHM of the booking system.
It generates available time slots for a given staff member, service, and date.

Algorithm:
1. Get the staff's schedule for the requested day of week
2. Generate candidate time slots at service-duration intervals
3. Fetch existing bookings for that staff + date
4. Remove slots that overlap with existing bookings
5. If the date is today, remove slots that are in the past
6. Return remaining available slots
"""

from datetime import date, datetime, time, timedelta
from typing import List, Tuple
from zoneinfo import ZoneInfo

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import settings
from app.models.booking import Booking, BookingStatus
from app.models.schedule import Schedule
from app.models.service import Service


async def get_staff_schedule_for_day(
    session: AsyncSession,
    staff_id,
    day_of_week: int,
) -> Schedule | None:
    """
    Get the schedule for a specific staff member on a specific day.

    Args:
        staff_id: UUID of the staff member
        day_of_week: 0=Monday, 6=Sunday

    Returns:
        Schedule object or None if staff doesn't work that day
    """
    result = await session.execute(
        select(Schedule).where(
            and_(
                Schedule.staff_id == staff_id,
                Schedule.day_of_week == day_of_week,
            )
        )
    )
    return result.scalar_one_or_none()


async def get_available_slots(
    session: AsyncSession,
    staff_id,
    service_id,
    target_date: date,
) -> List[Tuple[datetime, datetime]]:
    """
    Generate available time slots for booking.

    This is the core booking algorithm. It:
    1. Checks if the staff works on the given day
    2. Generates all possible time slots based on service duration
    3. Removes slots that conflict with existing bookings
    4. Removes past slots if the date is today

    Args:
        staff_id: UUID of the staff member
        service_id: UUID of the service
        target_date: The date to check availability for

    Returns:
        List of (start_time, end_time) datetime tuples representing available slots
    """
    tz = ZoneInfo(settings.timezone)
    now = datetime.now(tz)

    # 1. Get staff schedule for this day
    day_of_week = target_date.weekday()  # 0=Mon, 6=Sun
    schedule = await get_staff_schedule_for_day(session, staff_id, day_of_week)

    if schedule is None:
        return []  # Staff doesn't work this day

    # 2. Get service duration
    service_result = await session.execute(
        select(Service).where(Service.id == service_id)
    )
    service = service_result.scalar_one_or_none()
    if service is None:
        return []

    duration = timedelta(minutes=service.duration_minutes)

    # 3. Generate ALL candidate slots
    # Start from schedule start_time, increment by service duration
    work_start = datetime.combine(target_date, schedule.start_time, tzinfo=tz)
    work_end = datetime.combine(target_date, schedule.end_time, tzinfo=tz)

    candidates: List[Tuple[datetime, datetime]] = []
    slot_start = work_start

    while slot_start + duration <= work_end:
        slot_end = slot_start + duration
        candidates.append((slot_start, slot_end))
        slot_start = slot_end  # Next slot starts where this one ends

    # 4. Get existing bookings for this staff on this date
    day_start = datetime.combine(target_date, time.min, tzinfo=tz)
    day_end = datetime.combine(target_date, time.max, tzinfo=tz)

    bookings_result = await session.execute(
        select(Booking).where(
            and_(
                Booking.staff_id == staff_id,
                Booking.start_time >= day_start,
                Booking.end_time <= day_end,
                Booking.status.in_([
                    BookingStatus.PENDING,
                    BookingStatus.CONFIRMED,
                ]),
            )
        )
    )
    existing_bookings = bookings_result.scalars().all()

    # 5. Remove occupied slots (any overlap = unavailable)
    available: List[Tuple[datetime, datetime]] = []

    for slot_start, slot_end in candidates:
        is_occupied = False
        for booking in existing_bookings:
            # Two intervals overlap if one starts before the other ends
            if slot_start < booking.end_time and slot_end > booking.start_time:
                is_occupied = True
                break

        if not is_occupied:
            available.append((slot_start, slot_end))

    # 6. If today, remove past slots
    if target_date == now.date():
        available = [
            (start, end) for start, end in available
            if start > now
        ]

    return available


def get_available_dates(days_ahead: int = 7) -> List[date]:
    """
    Get a list of upcoming dates for the date picker.

    Args:
        days_ahead: Number of days to show (default 7)

    Returns:
        List of date objects starting from today
    """
    tz = ZoneInfo(settings.timezone)
    today = datetime.now(tz).date()
    return [today + timedelta(days=i) for i in range(days_ahead)]
