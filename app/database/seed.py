"""
Database seed script — populates demo data for multi-shop MVP.

Creates:
- 2 businesses (1 barbershop in Tashkent, 1 nail salon in Tashkent)
- Staff for each business
- Localized services (RU/UZ/EN names)
- Schedules (Mon-Sat 10:00-18:00)
"""

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

    result = await session.execute(select(Business).limit(1))
    if result.scalar_one_or_none() is not None:
        print("📦 Database already seeded, skipping.")
        return

    print("🌱 Seeding database with demo data...")

    # ═══════════════════════════════════════════════════════════════
    # BUSINESS 1: Barbershop
    # ═══════════════════════════════════════════════════════════════
    barbershop = Business(
        name="King Barber",
        category="barbershop",
        address="📍 Tashkent, Amir Temur ko'chasi 45",
        telegram_owner_id=settings.admin_telegram_id,
        phone="+998901234567",
    )
    session.add(barbershop)
    await session.flush()

    # Barbershop Staff
    barber_staff = []
    for name, role in [("Ali", "barber"), ("Bek", "barber"), ("Sardor", "barber")]:
        s = Staff(business_id=barbershop.id, name=name, role=role)
        session.add(s)
        barber_staff.append(s)
    await session.flush()

    # Barbershop Services (localized)
    barber_services = [
        {
            "name_ru": "✂️ Стрижка",
            "name_uz": "✂️ Soch olish",
            "name_en": "✂️ Haircut",
            "duration_minutes": 45,
            "price": 80000,
        },
        {
            "name_ru": "🧔 Борода",
            "name_uz": "🧔 Soqol olish",
            "name_en": "🧔 Beard Trim",
            "duration_minutes": 30,
            "price": 40000,
        },
        {
            "name_ru": "💈 Стрижка + Борода",
            "name_uz": "💈 Soch + Soqol",
            "name_en": "💈 Haircut + Beard",
            "duration_minutes": 60,
            "price": 110000,
        },
    ]
    for svc in barber_services:
        session.add(Service(business_id=barbershop.id, **svc))

    # Barbershop Schedules (Mon-Sat 10:00-18:00)
    for staff in barber_staff:
        for day in range(6):
            session.add(Schedule(staff_id=staff.id, day_of_week=day, start_time=time(10, 0), end_time=time(18, 0)))

    # ═══════════════════════════════════════════════════════════════
    # BUSINESS 2: Nail Salon
    # ═══════════════════════════════════════════════════════════════
    nail_salon = Business(
        name="Beauty Nails",
        category="nails",
        address="📍 Tashkent, Navoiy ko'chasi 12",
        telegram_owner_id=settings.admin_telegram_id,
        phone="+998901234568",
    )
    session.add(nail_salon)
    await session.flush()

    # Nail Salon Staff
    nail_staff = []
    for name, role in [("Madina", "master"), ("Dilfuza", "master")]:
        s = Staff(business_id=nail_salon.id, name=name, role=role)
        session.add(s)
        nail_staff.append(s)
    await session.flush()

    # Nail Salon Services (localized)
    nail_services = [
        {
            "name_ru": "💅 Маникюр",
            "name_uz": "💅 Manikur",
            "name_en": "💅 Manicure",
            "duration_minutes": 60,
            "price": 100000,
        },
        {
            "name_ru": "🦶 Педикюр",
            "name_uz": "🦶 Pedikur",
            "name_en": "🦶 Pedicure",
            "duration_minutes": 90,
            "price": 120000,
        },
        {
            "name_ru": "✨ Гель-лак",
            "name_uz": "✨ Gel-lak",
            "name_en": "✨ Gel Polish",
            "duration_minutes": 45,
            "price": 80000,
        },
        {
            "name_ru": "💎 Маникюр + Гель-лак",
            "name_uz": "💎 Manikur + Gel-lak",
            "name_en": "💎 Manicure + Gel Polish",
            "duration_minutes": 90,
            "price": 160000,
        },
    ]
    for svc in nail_services:
        session.add(Service(business_id=nail_salon.id, **svc))

    # Nail Salon Schedules (Mon-Sat 09:00-19:00)
    for staff in nail_staff:
        for day in range(6):
            session.add(Schedule(staff_id=staff.id, day_of_week=day, start_time=time(9, 0), end_time=time(19, 0)))

    await session.commit()
    print("✅ Demo data seeded:")
    print(f"   💈 {barbershop.name} — {barbershop.address}")
    print(f"      Staff: {', '.join(s.name for s in barber_staff)}")
    print(f"      Services: {len(barber_services)}")
    print(f"   💅 {nail_salon.name} — {nail_salon.address}")
    print(f"      Staff: {', '.join(s.name for s in nail_staff)}")
    print(f"      Services: {len(nail_services)}")
