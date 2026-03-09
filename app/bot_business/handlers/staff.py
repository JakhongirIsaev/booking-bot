"""
Staff handlers for Business Bot.
"""

from datetime import date, timedelta
from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.database.session import get_session
from app.services.staff_service import get_staff_by_telegram_id, get_staff_daily_bookings
from app.bot_business.keyboards.biz_kb import staff_main_menu, back_to_staff_menu

router = Router()


async def _show_schedule(callback: CallbackQuery, target_date: date, title: str) -> None:
    """Helper to display staff bookings for a given date."""
    user_id = callback.from_user.id

    async with get_session() as session:
        staff = await get_staff_by_telegram_id(session, user_id)
        if not staff:
            await callback.answer("You are not linked to a staff profile.", show_alert=True)
            return
            
        bookings = await get_staff_daily_bookings(session, staff.id, target_date)

    if not bookings:
        await callback.message.edit_text(
            f"📅 **{title} ({target_date.strftime('%d.%m.%Y')})**\n\n"
            f"You have no bookings for this day.",
            reply_markup=back_to_staff_menu(),
            parse_mode="Markdown",
        )
        await callback.answer()
        return

    text = f"📅 **{title} ({target_date.strftime('%d.%m.%Y')})**\n\n"
    
    for b in bookings:
        time_str = b.start_time.strftime("%H:%M")
        client_name = b.client.name if b.client else "Unknown"
        client_phone = b.client.phone if b.client and b.client.phone else "No phone"
        service = b.service.name_ru if b.service else "—"
        
        text += f"🕐 **{time_str}** — {client_name}\n"
        text += f"   💈 {service}\n"
        text += f"   📞 {client_phone}\n\n"

    await callback.message.edit_text(text, reply_markup=back_to_staff_menu(), parse_mode="Markdown")
    await callback.answer()


@router.callback_query(F.data == "staff:main_menu")
async def back_to_main(callback: CallbackQuery) -> None:
    """Return to staff main menu."""
    user_id = callback.from_user.id
    async with get_session() as session:
        staff = await get_staff_by_telegram_id(session, user_id)
    
    name = staff.name if staff else "Staff"
    await callback.message.edit_text(
        f"💈 Welcome back, {name}!\n\nHere's your staff panel:",
        reply_markup=staff_main_menu(),
    )
    await callback.answer()


@router.callback_query(F.data == "staff:today")
async def view_today(callback: CallbackQuery) -> None:
    """View today's bookings."""
    today = date.today()
    await _show_schedule(callback, today, "Today's Schedule")


@router.callback_query(F.data == "staff:tomorrow")
async def view_tomorrow(callback: CallbackQuery) -> None:
    """View tomorrow's bookings."""
    tomorrow = date.today() + timedelta(days=1)
    await _show_schedule(callback, tomorrow, "Tomorrow's Schedule")
