"""
Owner handlers for Business Bot.
"""

from datetime import date, datetime
from zoneinfo import ZoneInfo
from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.config.settings import settings
from app.database.session import get_session
from app.models.business import Business
from app.models.staff import Staff
from app.models.booking import Booking, BookingStatus
from app.services.staff_service import generate_link_code
from app.services.booking_service import get_bookings_for_date, get_all_upcoming_bookings
from app.bot_business.keyboards.biz_kb import (
    owner_main_menu, owner_staff_list, back_to_owner_menu,
    owner_bookings_submenu,
)
from app.i18n import t

router = Router()

# Simple in-memory owner language preference (per user)
_owner_lang: dict[int, str] = {}


def _get_owner_lang(user_id: int) -> str:
    return _owner_lang.get(user_id, "ru")


def set_owner_lang(user_id: int, lang: str) -> None:
    _owner_lang[user_id] = lang


def is_owner(user_id: int) -> bool:
    return user_id == settings.admin_telegram_id


# ─── Main Menu ──────────────────────────────────────────────────────

@router.callback_query(F.data == "owner:main_menu")
async def back_to_main(callback: CallbackQuery) -> None:
    """Return to owner main menu."""
    lang = _get_owner_lang(callback.from_user.id)
    await callback.message.edit_text(
        t("owner_welcome", lang),
        reply_markup=owner_main_menu(lang),
    )
    await callback.answer()


# ─── My Shops ───────────────────────────────────────────────────────

@router.callback_query(F.data == "owner:shops")
async def view_shops(callback: CallbackQuery) -> None:
    """List all businesses for the owner."""
    if not is_owner(callback.from_user.id):
        await callback.answer("Unauthorized", show_alert=True)
        return

    lang = _get_owner_lang(callback.from_user.id)
    async with get_session() as session:
        result = await session.execute(
            select(Business)
            .where(Business.telegram_owner_id == settings.admin_telegram_id)
            .order_by(Business.name)
        )
        shops = result.scalars().all()

    if not shops:
        await callback.message.edit_text(t("no_shops_owner", lang), reply_markup=back_to_owner_menu(lang))
        await callback.answer()
        return

    text = t("your_shops_title", lang)
    for s in shops:
        text += f"• **{s.name}** ({s.category})\n  📍 {s.address}\n\n"

    await callback.message.edit_text(text, reply_markup=back_to_owner_menu(lang), parse_mode="Markdown")
    await callback.answer()


# ─── My Staff ───────────────────────────────────────────────────────

@router.callback_query(F.data == "owner:staff")
async def view_staff(callback: CallbackQuery) -> None:
    """List all staff members and their link status."""
    if not is_owner(callback.from_user.id):
        await callback.answer("Unauthorized", show_alert=True)
        return

    lang = _get_owner_lang(callback.from_user.id)
    async with get_session() as session:
        result = await session.execute(
            select(Staff)
            .join(Staff.business)
            .where(Business.telegram_owner_id == settings.admin_telegram_id)
            .options(selectinload(Staff.business))
            .order_by(Business.name, Staff.name)
        )
        staff_list = result.scalars().all()

    if not staff_list:
        await callback.message.edit_text(t("no_staff_owner", lang), reply_markup=back_to_owner_menu(lang))
        await callback.answer()
        return

    await callback.message.edit_text(
        t("your_staff_title", lang),
        reply_markup=owner_staff_list(staff_list, lang),
        parse_mode="Markdown",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("owner:link_staff:"))
async def generate_staff_link(callback: CallbackQuery) -> None:
    """Generate and display a binding code for a specific staff member."""
    staff_id = callback.data.split(":")[2]
    lang = _get_owner_lang(callback.from_user.id)
    
    async with get_session() as session:
        code = await generate_link_code(session, staff_id)
        result = await session.execute(select(Staff).where(Staff.id == staff_id))
        staff = result.scalar_one_or_none()

    if not staff:
        await callback.answer("Error finding staff.", show_alert=True)
        return

    await callback.message.edit_text(
        t("staff_link_code", lang, name=staff.name, code=code),
        reply_markup=back_to_owner_menu(lang),
        parse_mode="Markdown",
    )
    await callback.answer()


# ─── Bookings ───────────────────────────────────────────────────────

@router.callback_query(F.data == "owner:bookings")
async def bookings_submenu(callback: CallbackQuery) -> None:
    """Show bookings sub-menu: today / upcoming."""
    if not is_owner(callback.from_user.id):
        await callback.answer("Unauthorized", show_alert=True)
        return

    lang = _get_owner_lang(callback.from_user.id)
    await callback.message.edit_text(
        t("btn_all_bookings", lang),
        reply_markup=owner_bookings_submenu(lang),
    )
    await callback.answer()


@router.callback_query(F.data == "owner:bookings_today")
async def bookings_today(callback: CallbackQuery) -> None:
    """Show today's bookings across all owner's shops."""
    if not is_owner(callback.from_user.id):
        await callback.answer("Unauthorized", show_alert=True)
        return

    lang = _get_owner_lang(callback.from_user.id)
    tz = ZoneInfo(settings.timezone)
    today = datetime.now(tz).date()

    async with get_session() as session:
        # Get all businesses
        biz_result = await session.execute(
            select(Business).where(Business.telegram_owner_id == settings.admin_telegram_id)
        )
        businesses = biz_result.scalars().all()

        all_bookings = []
        for biz in businesses:
            bookings = await get_bookings_for_date(session, biz.id, today)
            all_bookings.extend(bookings)

    if not all_bookings:
        await callback.message.edit_text(
            t("no_bookings_owner", lang),
            reply_markup=owner_bookings_submenu(lang),
        )
        await callback.answer()
        return

    text = t("owner_bookings_today", lang, date=today.strftime("%d.%m.%Y"))
    for b in sorted(all_bookings, key=lambda x: x.start_time):
        time_str = b.start_time.strftime("%H:%M")
        client_name = b.client.name if b.client else "—"
        client_phone = b.client.phone if b.client and b.client.phone else "—"
        staff_name = b.staff.name if b.staff else "—"
        
        if lang == "uz":
            service = b.service.name_uz if b.service else "—"
        elif lang == "en":
            service = b.service.name_en if b.service else "—"
        else:
            service = b.service.name_ru if b.service else "—"

        text += f"🕐 **{time_str}**\n"
        text += f"   👤 {client_name} ({client_phone})\n"
        text += f"   💈 {service}\n"
        text += f"   🧑‍💼 {staff_name}\n\n"

    await callback.message.edit_text(text, reply_markup=owner_bookings_submenu(lang), parse_mode="Markdown")
    await callback.answer()


@router.callback_query(F.data == "owner:bookings_upcoming")
async def bookings_upcoming(callback: CallbackQuery) -> None:
    """Show upcoming bookings across all owner's shops."""
    if not is_owner(callback.from_user.id):
        await callback.answer("Unauthorized", show_alert=True)
        return

    lang = _get_owner_lang(callback.from_user.id)

    async with get_session() as session:
        biz_result = await session.execute(
            select(Business).where(Business.telegram_owner_id == settings.admin_telegram_id)
        )
        businesses = biz_result.scalars().all()

        all_bookings = []
        for biz in businesses:
            bookings = await get_all_upcoming_bookings(session, biz.id, limit=10)
            all_bookings.extend(bookings)

    if not all_bookings:
        await callback.message.edit_text(
            t("no_bookings_owner", lang),
            reply_markup=owner_bookings_submenu(lang),
        )
        await callback.answer()
        return

    text = t("owner_bookings_upcoming", lang)
    for b in sorted(all_bookings, key=lambda x: x.start_time)[:20]:
        dt = b.start_time.strftime("%d.%m %H:%M")
        client_name = b.client.name if b.client else "—"
        staff_name = b.staff.name if b.staff else "—"
        
        if lang == "uz":
            service = b.service.name_uz if b.service else "—"
        elif lang == "en":
            service = b.service.name_en if b.service else "—"
        else:
            service = b.service.name_ru if b.service else "—"

        text += f"📅 **{dt}** — {client_name}\n"
        text += f"   💈 {service} | 🧑‍💼 {staff_name}\n\n"

    await callback.message.edit_text(text, reply_markup=owner_bookings_submenu(lang), parse_mode="Markdown")
    await callback.answer()
