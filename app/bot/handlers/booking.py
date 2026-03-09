"""
Booking flow handler — multi-step booking with i18n support.

Flow: Choose service → Choose barber → Choose date → Choose time → Confirm.
All text is displayed in the user's chosen language.
"""

from datetime import date as date_type, datetime
from zoneinfo import ZoneInfo

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from sqlalchemy import select

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
from app.i18n import t
from app.models.business import Business
from app.models.staff import Staff
from app.models.service import Service
from app.services.booking_service import create_booking
from app.services.client_service import get_or_create_client, get_client_language
from app.services.schedule_service import get_available_slots, get_available_dates

router = Router()


async def _get_lang(telegram_id: int) -> str:
    """Helper to get user's language from DB."""
    async with get_session() as session:
        return await get_client_language(session, telegram_id)


# ─── Step 1: Choose Service ─────────────────────────────────────────

@router.callback_query(F.data == "book_start")
async def start_booking(callback: CallbackQuery, state: FSMContext) -> None:
    """Start the booking flow — show service list."""
    await state.clear()
    lang = await _get_lang(callback.from_user.id)

    async with get_session() as session:
        result = await session.execute(
            select(Service).where(Service.is_active == True).order_by(Service.name)
        )
        services = result.scalars().all()

    if not services:
        await callback.message.edit_text(
            t("no_services", lang),
            reply_markup=main_menu_keyboard(lang),
            parse_mode="HTML",
        )
        await callback.answer()
        return

    await state.set_state(BookingStates.choosing_service)
    await callback.message.edit_text(
        t("choose_service", lang),
        reply_markup=services_keyboard(services, lang),
        parse_mode="HTML",
    )
    await callback.answer()


# ─── Step 2: Choose Staff ───────────────────────────────────────────

@router.callback_query(BookingStates.choosing_service, F.data.startswith("service:"))
async def choose_service(callback: CallbackQuery, state: FSMContext) -> None:
    """Service selected — show staff list."""
    service_id = callback.data.split(":")[1]
    await state.update_data(service_id=service_id)
    lang = await _get_lang(callback.from_user.id)

    async with get_session() as session:
        service_result = await session.execute(select(Service).where(Service.id == service_id))
        service = service_result.scalar_one_or_none()
        result = await session.execute(select(Staff).where(Staff.is_active == True).order_by(Staff.name))
        staff_list = result.scalars().all()

    if not staff_list:
        await callback.message.edit_text(t("no_staff", lang), reply_markup=main_menu_keyboard(lang), parse_mode="HTML")
        await callback.answer()
        return

    service_name = service.name if service else "—"
    await state.set_state(BookingStates.choosing_staff)
    await callback.message.edit_text(
        t("service_selected", lang, service=service_name),
        reply_markup=staff_keyboard(staff_list, lang),
        parse_mode="HTML",
    )
    await callback.answer()


# ─── Step 3: Choose Date ────────────────────────────────────────────

@router.callback_query(BookingStates.choosing_staff, F.data.startswith("staff:"))
async def choose_staff(callback: CallbackQuery, state: FSMContext) -> None:
    """Staff selected — show date picker."""
    staff_id = callback.data.split(":")[1]
    await state.update_data(staff_id=staff_id)
    lang = await _get_lang(callback.from_user.id)

    async with get_session() as session:
        staff_result = await session.execute(select(Staff).where(Staff.id == staff_id))
        staff = staff_result.scalar_one_or_none()

    dates = get_available_dates(days_ahead=7)
    staff_name = staff.name if staff else "—"

    await state.set_state(BookingStates.choosing_date)
    await callback.message.edit_text(
        t("staff_selected", lang, staff=staff_name),
        reply_markup=dates_keyboard(dates, lang),
        parse_mode="HTML",
    )
    await callback.answer()


# ─── Back to Staff ──────────────────────────────────────────────────

@router.callback_query(F.data == "back_to_staff")
async def back_to_staff(callback: CallbackQuery, state: FSMContext) -> None:
    lang = await _get_lang(callback.from_user.id)
    data = await state.get_data()

    async with get_session() as session:
        result = await session.execute(select(Staff).where(Staff.is_active == True).order_by(Staff.name))
        staff_list = result.scalars().all()
        service_result = await session.execute(select(Service).where(Service.id == data.get("service_id")))
        service = service_result.scalar_one_or_none()

    service_name = service.name if service else "—"
    await state.set_state(BookingStates.choosing_staff)
    await callback.message.edit_text(
        t("service_selected", lang, service=service_name),
        reply_markup=staff_keyboard(staff_list, lang),
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
    lang = await _get_lang(callback.from_user.id)

    data = await state.get_data()

    async with get_session() as session:
        slots = await get_available_slots(session, data["staff_id"], data["service_id"], target_date)

    if not slots:
        await callback.message.edit_text(
            t("no_slots", lang, date=target_date.strftime('%d.%m.%Y')),
            reply_markup=no_slots_keyboard(lang),
            parse_mode="HTML",
        )
        await callback.answer()
        return

    await state.set_state(BookingStates.choosing_time)
    await callback.message.edit_text(
        t("choose_time", lang, date=target_date.strftime('%d.%m.%Y')),
        reply_markup=time_slots_keyboard(slots, lang),
        parse_mode="HTML",
    )
    await callback.answer()


# ─── Back to Date ───────────────────────────────────────────────────

@router.callback_query(F.data == "back_to_date")
async def back_to_date(callback: CallbackQuery, state: FSMContext) -> None:
    lang = await _get_lang(callback.from_user.id)
    data = await state.get_data()

    async with get_session() as session:
        staff_result = await session.execute(select(Staff).where(Staff.id == data.get("staff_id")))
        staff = staff_result.scalar_one_or_none()

    dates = get_available_dates(days_ahead=7)
    staff_name = staff.name if staff else "—"

    await state.set_state(BookingStates.choosing_date)
    await callback.message.edit_text(
        t("staff_selected", lang, staff=staff_name),
        reply_markup=dates_keyboard(dates, lang),
        parse_mode="HTML",
    )
    await callback.answer()


# ─── Step 5: Confirm ────────────────────────────────────────────────

@router.callback_query(BookingStates.choosing_time, F.data.startswith("time:"))
async def choose_time(callback: CallbackQuery, state: FSMContext) -> None:
    """Time selected — show booking summary."""
    time_str = callback.data.split(":", 1)[1]
    await state.update_data(time=time_str)
    lang = await _get_lang(callback.from_user.id)
    data = await state.get_data()

    async with get_session() as session:
        service_result = await session.execute(select(Service).where(Service.id == data["service_id"]))
        service = service_result.scalar_one_or_none()
        staff_result = await session.execute(select(Staff).where(Staff.id == data["staff_id"]))
        staff = staff_result.scalar_one_or_none()

    service_name = service.name if service else "—"
    staff_name = staff.name if staff else "—"
    price = f"{int(service.price):,}".replace(",", " ") if service else "—"
    duration = f"{service.duration_minutes} {t('minutes', lang)}" if service else "—"

    start_dt = datetime.fromisoformat(time_str)

    await state.set_state(BookingStates.confirming)
    await callback.message.edit_text(
        t("booking_summary", lang,
          service=service_name, staff=staff_name,
          date=start_dt.strftime("%d.%m.%Y"), time=start_dt.strftime("%H:%M"),
          duration=duration, price=price),
        reply_markup=confirm_keyboard(lang),
        parse_mode="HTML",
    )
    await callback.answer()


# ─── Back to Time ───────────────────────────────────────────────────

@router.callback_query(F.data == "back_to_time")
async def back_to_time(callback: CallbackQuery, state: FSMContext) -> None:
    lang = await _get_lang(callback.from_user.id)
    data = await state.get_data()
    target_date = date_type.fromisoformat(data.get("date"))

    async with get_session() as session:
        slots = await get_available_slots(session, data["staff_id"], data["service_id"], target_date)

    if not slots:
        await callback.message.edit_text(
            t("no_slots_remaining", lang),
            reply_markup=no_slots_keyboard(lang), parse_mode="HTML",
        )
        await callback.answer()
        return

    await state.set_state(BookingStates.choosing_time)
    await callback.message.edit_text(
        t("choose_time", lang, date=target_date.strftime('%d.%m.%Y')),
        reply_markup=time_slots_keyboard(slots, lang), parse_mode="HTML",
    )
    await callback.answer()


# ─── Confirm Booking ────────────────────────────────────────────────

@router.callback_query(BookingStates.confirming, F.data == "confirm_yes")
async def confirm_booking(callback: CallbackQuery, state: FSMContext) -> None:
    """Confirm and save the booking to database."""
    data = await state.get_data()
    lang = await _get_lang(callback.from_user.id)

    start_time = datetime.fromisoformat(data["time"])
    tz = ZoneInfo(settings.timezone)
    if start_time.tzinfo is None:
        start_time = start_time.replace(tzinfo=tz)

    async with get_session() as session:
        client = await get_or_create_client(session, callback.from_user.id, callback.from_user.full_name or "User")
        business_result = await session.execute(select(Business).limit(1))
        business = business_result.scalar_one_or_none()

        if business is None:
            await callback.message.edit_text(t("error_business_not_found", lang), parse_mode="HTML")
            await state.clear()
            await callback.answer()
            return

        booking = await create_booking(session, business.id, client.id, data["staff_id"], data["service_id"], start_time)

        if booking is None:
            await callback.message.edit_text(
                t("slot_taken", lang), reply_markup=main_menu_keyboard(lang), parse_mode="HTML",
            )
            await state.clear()
            await callback.answer()
            return

        service_result = await session.execute(select(Service).where(Service.id == data["service_id"]))
        service = service_result.scalar_one_or_none()
        staff_result = await session.execute(select(Staff).where(Staff.id == data["staff_id"]))
        staff = staff_result.scalar_one_or_none()

    service_name = service.name if service else "—"
    staff_name = staff.name if staff else "—"

    await callback.message.edit_text(
        t("booking_confirmed", lang,
          service=service_name, staff=staff_name,
          date=start_time.strftime("%d.%m.%Y"), time=start_time.strftime("%H:%M"),
          business=settings.business_name),
        reply_markup=main_menu_keyboard(lang),
        parse_mode="HTML",
    )
    await state.clear()
    await callback.answer()


# ─── Cancel Booking Flow ────────────────────────────────────────────

@router.callback_query(F.data == "cancel_booking_flow")
async def cancel_booking_flow(callback: CallbackQuery, state: FSMContext) -> None:
    """Cancel the booking flow and return to main menu."""
    await state.clear()
    lang = await _get_lang(callback.from_user.id)

    await callback.message.edit_text(
        t("booking_cancelled_flow", lang, business=settings.business_name),
        reply_markup=main_menu_keyboard(lang),
        parse_mode="HTML",
    )
    await callback.answer()
