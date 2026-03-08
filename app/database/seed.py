"""
Database seed script — populates demo data for MVP testing.

Creates:
- 1 business (Demo Barbershop)
- 3 staff members (Ali, Bek, Sardor)
- 3 services (Haircut, Beard Trim, Haircut + Beard)
- Schedules (Mon-Sat 10:00-18:00 for all staff)

Run this on first startup if the database is empty.
"""

import uuid
from datetime import time

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.business import Business
from app.models.staff import Staff
from app.models.service import Service
from app.models.schedule import Schedule
from app.config.settings import settings


async def seed_database(session: AsyncSession) -> None:
    """Populate database with demo data if empty."""

    # Check if data already exists
    result = await session.execute(select(Business).limit(1))
    if result.scalar_one_or_none() is not None:
        print("📦 Database already seeded, skipping.")
        return

    print("🌱 Seeding database with demo data...")

    # --- Business ---
    business = Business(
        name=settings.business_name,
        telegram_owner_id=settings.admin_telegram_id,
        phone="+998901234567",
    )
    session.add(business)
    await session.flush()  # Get the business.id

    # --- Staff ---
    staff_data = [
        {"name": "Ali", "role": "barber"},
        {"name": "Bek", "role": "barber"},
        {"name": "Sardor", "role": "barber"},
    ]
    staff_members = []
    for data in staff_data:
        staff = Staff(
            business_id=business.id,
            name=data["name"],
            role=data["role"],
        )
        session.add(staff)
        staff_members.append(staff)
    await session.flush()

    # --- Services ---
    services_data = [
        {
            "name": "✂️ Haircut",
            "description": "Classic haircut",
            "duration_minutes": 45,
            "price": 80000,
        },
        {
            "name": "🧔 Beard Trim",
            "description": "Professional beard trim and shaping",
            "duration_minutes": 30,
            "price": 40000,
        },
        {
            "name": "💈 Haircut + Beard",
            "description": "Full haircut and beard trim combo",
            "duration_minutes": 60,
            "price": 110000,
        },
    ]
    for data in services_data:
        service = Service(
            business_id=business.id,
            name=data["name"],
            description=data["description"],
            duration_minutes=data["duration_minutes"],
            price=data["price"],
        )
        session.add(service)

    # --- Schedules (Mon-Sat 10:00-18:00 for all staff) ---
    for staff in staff_members:
        for day in range(6):  # 0=Mon to 5=Sat
            schedule = Schedule(
                staff_id=staff.id,
                day_of_week=day,
                start_time=time(10, 0),
                end_time=time(18, 0),
            )
            session.add(schedule)

    await session.commit()
    print("✅ Demo data seeded successfully!")
    print(f"   Business: {business.name}")
    print(f"   Staff: {', '.join(s.name for s in staff_members)}")
    print(f"   Services: {len(services_data)}")
    print(f"   Schedules: Mon-Sat 10:00-18:00")
