"""
Booking flow handler — the complete multi-step booking conversation.

This is the main booking FSM that guides users through:
  1. Choose a service (Haircut, Beard Trim, etc.)
  2. Choose a barber (Ali, Bek, Sardor)
  3. Choose a date (next 7 days)
  4. Choose an available time slot
  5. Confirm and save the booking

Each step uses inline keyboards for selection.
The FSM state machine tracks progress per-user.

IMPORTANT: Business logic is NOT in these handlers.
Handlers only call services from app.services.
"""

from datetime import date as date_type, datetime
from zoneinfo import ZoneInfo

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from app.bot.states import BookingStates
from app.bot.keyboards.client_kb import (
    services_keyboard,
    staff_keyboard,
    dates_keyboard,
    time_slots_keyboard,
    confirm_keyboard,
    main_menu_keyboard,
    no_slots_keyboard,
)
from app.config.settings import settings
from app.database.session import get_session
from app.models.business import Business
from app.models.staff import Staff
from app.models.service import Service
from app.services.booking_service import create_booking
from app.services.client_service import get_or_create_client
from app.services.schedule_service import get_available_slots, get_available_dates

from sqlalchemy import select

router = Router()


# ─── Step 1: Choose Service ─────────────────────────────────────────

@router.callback_query(F.data == "book_start")
async def start_booking(callback: CallbackQuery, state: FSMContext) -> None:
    """Start the booking flow — show service list."""
    await state.clear()

    async with get_session() as session:
        # Get all active services for the business
        result = await session.execute(
            select(Service).where(Service.is_active == True).order_by(Service.name)
        )
        services = result.scalars().all()

    if not services:
        await callback.message.edit_text(
            "❌ No services available at the moment.",
            reply_markup=main_menu_keyboard(),
            parse_mode="HTML",
        )
        await callback.answer()
        return

    await state.set_state(BookingStates.choosing_service)

    await callback.message.edit_text(
        "💈 <b>Choose a service:</b>",
        reply_markup=services_keyboard(services),
        parse_mode="HTML",
    )
    await callback.answer()


# ─── Step 2: Choose Staff ───────────────────────────────────────────

@router.callback_query(BookingStates.choosing_service, F.data.startswith("service:"))
async def choose_service(callback: CallbackQuery, state: FSMContext) -> None:
    """Service selected — show staff list."""
    service_id = callback.data.split(":")[1]
    await state.update_data(service_id=service_id)

    async with get_session() as session:
        # Get the selected service details
        service_result = await session.execute(
            select(Service).where(Service.id == service_id)
        )
        service = service_result.scalar_one_or_none()

        # Get all active staff
        result = await session.execute(
            select(Staff).where(Staff.is_active == True).order_by(Staff.name)
        )
        staff_list = result.scalars().all()

    if not staff_list:
        await callback.message.edit_text(
            "❌ No staff available at the moment.",
            reply_markup=main_menu_keyboard(),
            parse_mode="HTML",
        )
        await callback.answer()
        return

    service_name = service.name if service else "Service"
    await state.set_state(BookingStates.choosing_staff)

    await callback.message.edit_text(
        f"✅ Service: <b>{service_name}</b>\n\n"
        f"👤 <b>Choose a barber:</b>",
        reply_markup=staff_keyboard(staff_list),
        parse_mode="HTML",
    )
    await callback.answer()


# ─── Step 3: Choose Date ────────────────────────────────────────────

@router.callback_query(BookingStates.choosing_staff, F.data.startswith("staff:"))
async def choose_staff(callback: CallbackQuery, state: FSMContext) -> None:
    """Staff selected — show date picker."""
    staff_id = callback.data.split(":")[1]
    await state.update_data(staff_id=staff_id)

    async with get_session() as session:
        staff_result = await session.execute(
            select(Staff).where(Staff.id == staff_id)
        )
        staff = staff_result.scalar_one_or_none()

    dates = get_available_dates(days_ahead=7)
    staff_name = staff.name if staff else "Barber"

    await state.set_state(BookingStates.choosing_date)

    await callback.message.edit_text(
        f"👤 Barber: <b>{staff_name}</b>\n\n"
        f"📅 <b>Choose a date:</b>",
        reply_markup=dates_keyboard(dates),
        parse_mode="HTML",
    )
    await callback.answer()


# ─── Back Navigation: Back to Staff ─────────────────────────────────

@router.callback_query(F.data == "back_to_staff")
async def back_to_staff(callback: CallbackQuery, state: FSMContext) -> None:
    """Navigate back to staff selection."""
    async with get_session() as session:
        result = await session.execute(
            select(Staff).where(Staff.is_active == True).order_by(Staff.name)
        )
        staff_list = result.scalars().all()

    data = await state.get_data()
    service_id = data.get("service_id")

    async with get_session() as session:
        service_result = await session.execute(
            select(Service).where(Service.id == service_id)
        )
        service = service_result.scalar_one_or_none()

    service_name = service.name if service else "Service"
    await state.set_state(BookingStates.choosing_staff)

    await callback.message.edit_text(
        f"✅ Service: <b>{service_name}</b>\n\n"
        f"👤 <b>Choose a barber:</b>",
        reply_markup=staff_keyboard(staff_list),
        parse_mode="HTML",
    )
    await callback.answer()


# ─── Step 4: Choose Time ────────────────────────────────────────────

@router.callback_query(BookingStates.choosing_date, F.data.startswith("date:"))
async def choose_date(callback: CallbackQuery, state: FSMContext) -> None:
    """Date selected — show available time slots."""
    date_str = callback.data.split(":")[1]
    target_date = date_type.fromisoformat(date_str)
    await state.update_data(date=date_str)

    data = await state.get_data()
    staff_id = data["staff_id"]
    service_id = data["service_id"]

    async with get_session() as session:
        slots = await get_available_slots(
            session=session,
            staff_id=staff_id,
            service_id=service_id,
            target_date=target_date,
        )

    if not slots:
        await callback.message.edit_text(
            f"😔 <b>No available slots</b> on {target_date.strftime('%d.%m.%Y')}.\n\n"
            f"Try a different date.",
            reply_markup=no_slots_keyboard(),
            parse_mode="HTML",
        )
        await callback.answer()
        return

    await state.set_state(BookingStates.choosing_time)

    date_display = target_date.strftime("%d.%m.%Y")
    await callback.message.edit_text(
        f"📅 Date: <b>{date_display}</b>\n\n"
        f"🕐 <b>Choose a time:</b>",
        reply_markup=time_slots_keyboard(slots),
        parse_mode="HTML",
    )
    await callback.answer()


# ─── Back Navigation: Back to Date ──────────────────────────────────

@router.callback_query(F.data == "back_to_date")
async def back_to_date(callback: CallbackQuery, state: FSMContext) -> None:
    """Navigate back to date selection."""
    data = await state.get_data()
    staff_id = data.get("staff_id")

    async with get_session() as session:
        staff_result = await session.execute(
            select(Staff).where(Staff.id == staff_id)
        )
        staff = staff_result.scalar_one_or_none()

    dates = get_available_dates(days_ahead=7)
    staff_name = staff.name if staff else "Barber"

    await state.set_state(BookingStates.choosing_date)

    await callback.message.edit_text(
        f"👤 Barber: <b>{staff_name}</b>\n\n"
        f"📅 <b>Choose a date:</b>",
        reply_markup=dates_keyboard(dates),
        parse_mode="HTML",
    )
    await callback.answer()


# ─── Step 5: Confirm Booking ────────────────────────────────────────

@router.callback_query(BookingStates.choosing_time, F.data.startswith("time:"))
async def choose_time(callback: CallbackQuery, state: FSMContext) -> None:
    """Time selected — show booking summary for confirmation."""
    time_str = callback.data.split(":", 1)[1]
    await state.update_data(time=time_str)

    data = await state.get_data()

    async with get_session() as session:
        # Fetch service and staff names for display
        service_result = await session.execute(
            select(Service).where(Service.id == data["service_id"])
        )
        service = service_result.scalar_one_or_none()

        staff_result = await session.execute(
            select(Staff).where(Staff.id == data["staff_id"])
        )
        staff = staff_result.scalar_one_or_none()

    service_name = service.name if service else "Service"
    staff_name = staff.name if staff else "Barber"
    price = f"{int(service.price):,}".replace(",", " ") if service else "—"
    duration = f"{service.duration_minutes} min" if service else "—"

    # Parse time for display
    start_dt = datetime.fromisoformat(time_str)
    date_display = start_dt.strftime("%d.%m.%Y")
    time_display = start_dt.strftime("%H:%M")

    await state.set_state(BookingStates.confirming)

    summary = (
        f"📋 <b>Booking Summary</b>\n\n"
        f"💈 Service: <b>{service_name}</b>\n"
        f"👤 Barber: <b>{staff_name}</b>\n"
        f"📅 Date: <b>{date_display}</b>\n"
        f"🕐 Time: <b>{time_display}</b>\n"
        f"⏱ Duration: <b>{duration}</b>\n"
        f"💰 Price: <b>{price} сум</b>\n\n"
        f"Confirm your booking?"
    )

    await callback.message.edit_text(
        summary,
        reply_markup=confirm_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer()


# ─── Back Navigation: Back to Time ──────────────────────────────────

@router.callback_query(F.data == "back_to_time")
async def back_to_time(callback: CallbackQuery, state: FSMContext) -> None:
    """Navigate back to time slot selection."""
    data = await state.get_data()
    staff_id = data.get("staff_id")
    service_id = data.get("service_id")
    date_str = data.get("date")

    target_date = date_type.fromisoformat(date_str)

    async with get_session() as session:
        slots = await get_available_slots(
            session=session,
            staff_id=staff_id,
            service_id=service_id,
            target_date=target_date,
        )

    if not slots:
        await callback.message.edit_text(
            "😔 <b>No available slots</b> remaining.\n\nTry a different date.",
            reply_markup=no_slots_keyboard(),
            parse_mode="HTML",
        )
        await callback.answer()
        return

    await state.set_state(BookingStates.choosing_time)

    date_display = target_date.strftime("%d.%m.%Y")
    await callback.message.edit_text(
        f"📅 Date: <b>{date_display}</b>\n\n"
        f"🕐 <b>Choose a time:</b>",
        reply_markup=time_slots_keyboard(slots),
        parse_mode="HTML",
    )
    await callback.answer()


# ─── Confirm Booking ────────────────────────────────────────────────

@router.callback_query(BookingStates.confirming, F.data == "confirm_yes")
async def confirm_booking(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Confirm and save the booking.

    This is where the booking is actually created in the database.
    Includes conflict detection (if someone booked the slot while user was deciding).
    """
    data = await state.get_data()

    start_time = datetime.fromisoformat(data["time"])
    tz = ZoneInfo(settings.timezone)
    if start_time.tzinfo is None:
        start_time = start_time.replace(tzinfo=tz)

    async with get_session() as session:
        # Get or create client
        client = await get_or_create_client(
            session=session,
            telegram_id=callback.from_user.id,
            name=callback.from_user.full_name or "Unknown",
        )

        # Get business
        business_result = await session.execute(select(Business).limit(1))
        business = business_result.scalar_one_or_none()

        if business is None:
            await callback.message.edit_text(
                "❌ Error: Business not found. Contact admin.",
                parse_mode="HTML",
            )
            await state.clear()
            await callback.answer()
            return

        # Create booking
        booking = await create_booking(
            session=session,
            business_id=business.id,
            client_id=client.id,
            staff_id=data["staff_id"],
            service_id=data["service_id"],
            start_time=start_time,
        )

        if booking is None:
            await callback.message.edit_text(
                "😔 <b>Sorry, this slot is no longer available.</b>\n\n"
                "Someone else booked it while you were deciding.\n"
                "Please try again.",
                reply_markup=main_menu_keyboard(),
                parse_mode="HTML",
            )
            await state.clear()
            await callback.answer()
            return

        # Fetch names for confirmation message
        service_result = await session.execute(
            select(Service).where(Service.id == data["service_id"])
        )
        service = service_result.scalar_one_or_none()

        staff_result = await session.execute(
            select(Staff).where(Staff.id == data["staff_id"])
        )
        staff = staff_result.scalar_one_or_none()

    service_name = service.name if service else "Service"
    staff_name = staff.name if staff else "Barber"
    date_display = start_time.strftime("%d.%m.%Y")
    time_display = start_time.strftime("%H:%M")

    success_message = (
        f"✅ <b>Booking Confirmed!</b>\n\n"
        f"💈 Service: <b>{service_name}</b>\n"
        f"👤 Barber: <b>{staff_name}</b>\n"
        f"📅 Date: <b>{date_display}</b>\n"
        f"🕐 Time: <b>{time_display}</b>\n\n"
        f"See you at <b>{settings.business_name}</b>! 💈"
    )

    await callback.message.edit_text(
        success_message,
        reply_markup=main_menu_keyboard(),
        parse_mode="HTML",
    )
    await state.clear()
    await callback.answer("✅ Booking confirmed!")


# ─── Cancel Booking Flow ────────────────────────────────────────────

@router.callback_query(F.data == "cancel_booking_flow")
async def cancel_booking_flow(callback: CallbackQuery, state: FSMContext) -> None:
    """Cancel the booking flow and return to main menu."""
    await state.clear()

    await callback.message.edit_text(
        f"❌ Booking cancelled.\n\n"
        f"👋 <b>{settings.business_name}</b>\n"
        f"Choose an option:",
        reply_markup=main_menu_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer()
