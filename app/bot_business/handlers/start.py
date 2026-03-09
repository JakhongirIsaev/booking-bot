"""
Start handler for Business Bot.
"""

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from app.config.settings import settings
from app.database.session import get_session
from app.services.staff_service import get_staff_by_telegram_id, link_telegram_account
from app.bot_business.keyboards.biz_kb import owner_main_menu, staff_main_menu, lang_picker_kb
from app.bot_business.handlers.owner import _get_owner_lang, set_owner_lang
from app.i18n import t

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    """Welcome the user and route them based on their role."""
    user_id = message.from_user.id

    # 1. Check if Owner
    if user_id == settings.admin_telegram_id:
        lang = _get_owner_lang(user_id)
        await message.answer(
            t("owner_welcome", lang),
            reply_markup=owner_main_menu(lang),
        )
        return

    # 2. Check if Staff
    async with get_session() as session:
        staff = await get_staff_by_telegram_id(session, user_id)

    if staff:
        lang = staff.language
        await message.answer(
            t("staff_welcome", lang, name=staff.name),
            reply_markup=staff_main_menu(lang),
        )
        return

    # 3. Unlinked user — show language picker first, then unlinked message
    await message.answer(
        "🌐 Выберите язык / Tilni tanlang / Choose your language:",
        reply_markup=lang_picker_kb(),
    )


@router.message(Command("link"))
async def cmd_link(message: Message) -> None:
    """Link a staff profile using a code."""
    args = message.text.split(" ")
    if len(args) < 2:
        await message.answer(t("link_no_code", "ru"), parse_mode="Markdown")
        return

    code = args[1].strip().upper()
    user_id = message.from_user.id

    async with get_session() as session:
        staff = await link_telegram_account(session, code, user_id)

    if not staff:
        await message.answer(t("link_invalid", "ru"))
        return

    lang = staff.language
    await message.answer(
        t("link_success", lang, name=staff.name),
        reply_markup=staff_main_menu(lang),
        parse_mode="Markdown",
    )


# ─── Language Change for Staff & Owner ──────────────────────────────

@router.callback_query(F.data == "biz_lang_picker")
async def biz_change_language_picker(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        "🌐 Выберите язык / Tilni tanlang / Choose your language:",
        reply_markup=lang_picker_kb(),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("biz_lang:"))
async def biz_set_language(callback: CallbackQuery) -> None:
    lang = callback.data.split(":")[1]
    user_id = callback.from_user.id
    
    # Check if Owner
    if user_id == settings.admin_telegram_id:
        set_owner_lang(user_id, lang)
        await callback.message.edit_text(
            t("owner_welcome", lang),
            reply_markup=owner_main_menu(lang),
        )
        await callback.answer()
        return
    
    # Check if Staff
    async with get_session() as session:
        staff = await get_staff_by_telegram_id(session, user_id)
        if staff:
            staff.language = lang
            await session.commit()
            
            await callback.message.edit_text(
                t("staff_welcome", lang, name=staff.name),
                reply_markup=staff_main_menu(lang),
            )
        else:
            # Unlinked user who just chose language
            await callback.message.edit_text(
                t("unlinked_msg", lang),
                parse_mode="Markdown",
            )
            
    await callback.answer()
