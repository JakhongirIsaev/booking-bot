"""
Owner handlers for Business Bot.
"""

from datetime import date
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database.session import get_session
from app.models.business import Business
from app.models.staff import Staff
from app.services.staff_service import generate_link_code
from app.bot_business.keyboards.biz_kb import owner_main_menu, owner_staff_list, back_to_owner_menu
from app.i18n import t

router = Router()


# Define a simple filter to only allow the configured admin ID
def is_owner(user_id: int, admin_id: int) -> bool:
    return user_id == admin_id


@router.callback_query(F.data == "owner:main_menu")
async def back_to_main(callback: CallbackQuery) -> None:
    """Return to owner main menu."""
    lang = "ru"
    await callback.message.edit_text(
        t("owner_welcome", lang),
        reply_markup=owner_main_menu(lang),
    )
    await callback.answer()


@router.callback_query(F.data == "owner:shops")
async def view_shops(callback: CallbackQuery) -> None:
    """List all businesses for the owner."""
    from app.config.settings import settings
    if not is_owner(callback.from_user.id, settings.admin_telegram_id):
        await callback.answer("Unauthorized", show_alert=True)
        return

    lang = "ru"
    async with get_session() as session:
        result = await session.execute(
            select(Business)
            .where(Business.telegram_owner_id == settings.admin_telegram_id)
            .order_by(Business.name)
        )
        shops = result.scalars().all()

    if not shops:
        await callback.message.edit_text(t("no_shops_owner", lang), reply_markup=back_to_owner_menu(lang))
        return

    text = t("your_shops_title", lang)
    for s in shops:
        text += f"• **{s.name}** ({s.category})\n  {s.address}\n\n"

    await callback.message.edit_text(text, reply_markup=back_to_owner_menu(lang), parse_mode="Markdown")
    await callback.answer()


@router.callback_query(F.data == "owner:staff")
async def view_staff(callback: CallbackQuery) -> None:
    """List all staff members and their link status."""
    from app.config.settings import settings
    if not is_owner(callback.from_user.id, settings.admin_telegram_id):
        await callback.answer("Unauthorized", show_alert=True)
        return

    lang = "ru"
    async with get_session() as session:
        # Get staff for all businesses owned by this admin
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
    lang = "ru"
    
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
