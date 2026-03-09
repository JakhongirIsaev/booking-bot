"""
Staff handlers for Business Bot.
"""

from datetime import date, timedelta
from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.database.session import get_session
from app.services.staff_service import get_staff_by_telegram_id, get_staff_daily_bookings
from app.bot_business.keyboards.biz_kb import staff_main_menu, back_to_staff_menu
from app.i18n import t

router = Router()


async def _show_schedule(callback: CallbackQuery, target_date: date, title_key: str) -> None:
    """Helper to display staff bookings for a given date."""
    user_id = callback.from_user.id

    async with get_session() as session:
        staff = await get_staff_by_telegram_id(session, user_id)
        if not staff:
            await callback.answer("You are not linked to a staff profile.", show_alert=True)
            return
            
        bookings = await get_staff_daily_bookings(session, staff.id, target_date)
        lang = staff.language

    date_str = target_date.strftime('%d.%m.%Y')
    title_text = t(title_key, lang)
    
    if not bookings:
        await callback.message.edit_text(
            t("no_bookings_day", lang, title=title_text, date=date_str),
            reply_markup=back_to_staff_menu(lang),
            parse_mode="Markdown",
        )
        await callback.answer()
        return

    text = t("schedule_title", lang, title=title_text, date=date_str)
    
    for b in bookings:
        time_str = b.start_time.strftime("%H:%M")
        client_name = b.client.name if b.client else "Unknown"
        client_phone = b.client.phone if b.client and b.client.phone else "—"
        
        if lang == "ru":
            service = b.service.name_ru if b.service else "—"
        elif lang == "uz":
            service = b.service.name_uz if b.service else "—"
        else:
            service = b.service.name_en if b.service else "—"
        
        text += f"🕐 **{time_str}** — {client_name}\n"
        text += f"   💈 {service}\n"
        text += f"   📞 {client_phone}\n\n"

    await callback.message.edit_text(text, reply_markup=back_to_staff_menu(lang), parse_mode="Markdown")
    await callback.answer()


@router.callback_query(F.data == "staff:main_menu")
async def back_to_main(callback: CallbackQuery) -> None:
    """Return to staff main menu."""
    user_id = callback.from_user.id
    async with get_session() as session:
        staff = await get_staff_by_telegram_id(session, user_id)
    
    name = staff.name if staff else "Staff"
    lang = staff.language if staff else "ru"
    
    await callback.message.edit_text(
        t("staff_welcome", lang, name=name),
        reply_markup=staff_main_menu(lang),
    )
    await callback.answer()


@router.callback_query(F.data == "staff:today")
async def view_today(callback: CallbackQuery) -> None:
    """View today's bookings."""
    today = date.today()
    await _show_schedule(callback, today, "title_today")


@router.callback_query(F.data == "staff:tomorrow")
async def view_tomorrow(callback: CallbackQuery) -> None:
    """View tomorrow's bookings."""
    tomorrow = date.today() + timedelta(days=1)
    await _show_schedule(callback, tomorrow, "title_tomorrow")
