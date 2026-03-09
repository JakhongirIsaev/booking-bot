"""
Staff Service — manages staff records and schedules for the business bot.
"""

import random
import string
from datetime import date, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.staff import Staff
from app.models.booking import Booking


async def get_staff_by_telegram_id(session: AsyncSession, telegram_id: int) -> Staff | None:
    """Find a staff member by their connected Telegram ID."""
    result = await session.execute(
        select(Staff)
        .where(Staff.telegram_id == telegram_id, Staff.is_active == True)
        .options(selectinload(Staff.business))
    )
    return result.scalar_one_or_none()


async def generate_link_code(session: AsyncSession, staff_id: str) -> str | None:
    """Generate a unique 6-character code for linking a staff Telegram account."""
    result = await session.execute(select(Staff).where(Staff.id == staff_id))
    staff = result.scalar_one_or_none()
    
    if not staff:
        return None

    code = "BARBER-" + "".join(random.choices(string.digits, k=4))
    staff.link_code = code
    await session.commit()
    return code


async def link_telegram_account(session: AsyncSession, code: str, telegram_id: int) -> Staff | None:
    """Link a Telegram ID to a staff member using a code."""
    result = await session.execute(select(Staff).where(Staff.link_code == code))
    staff = result.scalar_one_or_none()

    if not staff:
        return None

    staff.telegram_id = telegram_id
    staff.link_code = None  # Use once
    await session.commit()
    return staff


async def get_staff_daily_bookings(session: AsyncSession, staff_id: str, target_date: date) -> list[Booking]:
    """Get all bookings for a staff member on a specific date."""
    start_of_day = datetime.combine(target_date, datetime.min.time())
    end_of_day = datetime.combine(target_date, datetime.max.time())

    result = await session.execute(
        select(Booking)
        .where(
            Booking.staff_id == staff_id,
            Booking.start_time >= start_of_day,
            Booking.start_time <= end_of_day,
            Booking.status != "cancelled"
        )
        .options(selectinload(Booking.service))
        .order_by(Booking.start_time)
    )
    return list(result.scalars().all())
