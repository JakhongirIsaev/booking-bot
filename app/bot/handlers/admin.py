"""
Admin handler — business owner's management interface.

Provides:
- /admin command — access admin menu (restricted to ADMIN_TELEGRAM_ID)
- Today's bookings list
- All upcoming bookings
- Basic statistics

Access control: Only the user whose Telegram ID matches
ADMIN_TELEGRAM_ID in settings can access these features.
"""

from datetime import datetime
from zoneinfo import ZoneInfo

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from sqlalchemy import select

from app.config.settings import settings
from app.database.session import get_session
from app.models.business import Business
from app.services.booking_service import (
    get_bookings_for_date,
    get_all_upcoming_bookings,
    get_booking_stats,
)
from app.bot.keyboards.admin_kb import admin_menu_keyboard
from app.bot.keyboards.client_kb import main_menu_keyboard

router = Router()


def is_admin(telegram_id: int) -> bool:
    """Check if the user is the admin."""
    return telegram_id == settings.admin_telegram_id


@router.message(Command("admin"))
async def cmd_admin(message: Message) -> None:
    """
    /admin command — show admin menu.
    Only accessible by the business owner.
    """
    if not is_admin(message.from_user.id):
        await message.answer(
            "⛔ Access denied.\n"
            "This command is only for the business admin.",
            parse_mode="HTML",
        )
        return

    await message.answer(
        f"🔧 <b>Admin Panel — {settings.business_name}</b>\n\n"
        f"Choose an action:",
        reply_markup=admin_menu_keyboard(),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "admin_today")
async def admin_today_bookings(callback: CallbackQuery) -> None:
    """Show today's bookings."""
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access denied.", show_alert=True)
        return

    tz = ZoneInfo(settings.timezone)
    today = datetime.now(tz).date()

    async with get_session() as session:
        business_result = await session.execute(select(Business).limit(1))
        business = business_result.scalar_one_or_none()

        if business is None:
            await callback.answer("❌ Business not found.", show_alert=True)
            return

        bookings = await get_bookings_for_date(
            session=session,
            business_id=business.id,
            target_date=today,
        )

    if not bookings:
        text = (
            f"📅 <b>Today's Bookings</b> ({today.strftime('%d.%m.%Y')})\n\n"
            f"No bookings for today."
        )
    else:
        lines = [f"📅 <b>Today's Bookings</b> ({today.strftime('%d.%m.%Y')})\n"]
        for i, booking in enumerate(bookings, 1):
            time_str = booking.start_time.strftime("%H:%M")
            service_name = booking.service.name if booking.service else "—"
            staff_name = booking.staff.name if booking.staff else "—"
            client_name = booking.client.name if booking.client else "—"
            status = booking.status.value.upper()

            lines.append(
                f"\n<b>{i}.</b> 🕐 {time_str}\n"
                f"   💈 {service_name}\n"
                f"   👤 Barber: {staff_name}\n"
                f"   👥 Client: {client_name}\n"
                f"   📌 Status: {status}"
            )

        text = "\n".join(lines)

    await callback.message.edit_text(
        text,
        reply_markup=admin_menu_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "admin_upcoming")
async def admin_upcoming_bookings(callback: CallbackQuery) -> None:
    """Show all upcoming bookings."""
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access denied.", show_alert=True)
        return

    async with get_session() as session:
        business_result = await session.execute(select(Business).limit(1))
        business = business_result.scalar_one_or_none()

        if business is None:
            await callback.answer("❌ Business not found.", show_alert=True)
            return

        bookings = await get_all_upcoming_bookings(
            session=session,
            business_id=business.id,
            limit=15,
        )

    if not bookings:
        text = "📋 <b>Upcoming Bookings</b>\n\nNo upcoming bookings."
    else:
        lines = [f"📋 <b>Upcoming Bookings</b> (next {len(bookings)})\n"]
        for i, booking in enumerate(bookings, 1):
            date_str = booking.start_time.strftime("%d.%m")
            time_str = booking.start_time.strftime("%H:%M")
            service_name = booking.service.name if booking.service else "—"
            staff_name = booking.staff.name if booking.staff else "—"
            client_name = booking.client.name if booking.client else "—"

            lines.append(
                f"\n<b>{i}.</b> 📅 {date_str} 🕐 {time_str}\n"
                f"   💈 {service_name} | 👤 {staff_name}\n"
                f"   👥 Client: {client_name}"
            )

        text = "\n".join(lines)

    await callback.message.edit_text(
        text,
        reply_markup=admin_menu_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "admin_stats")
async def admin_statistics(callback: CallbackQuery) -> None:
    """Show basic business statistics."""
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Access denied.", show_alert=True)
        return

    async with get_session() as session:
        business_result = await session.execute(select(Business).limit(1))
        business = business_result.scalar_one_or_none()

        if business is None:
            await callback.answer("❌ Business not found.", show_alert=True)
            return

        stats = await get_booking_stats(
            session=session,
            business_id=business.id,
        )

    text = (
        f"📊 <b>Statistics — {settings.business_name}</b>\n\n"
        f"📅 Today's bookings: <b>{stats['today_bookings']}</b>\n"
        f"📋 Total bookings: <b>{stats['total_bookings']}</b>\n"
        f"👥 Total clients: <b>{stats['total_clients']}</b>"
    )

    await callback.message.edit_text(
        text,
        reply_markup=admin_menu_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer()
