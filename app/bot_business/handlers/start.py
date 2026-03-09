"""
Start handler for Business Bot.

Determines user role:
1. Owner (telegram_id matches settings.admin_telegram_id)
2. Staff (telegram_id linked in staff table)
3. Unlinked (prompts to enter /link <code)
"""

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from app.config.settings import settings
from app.database.session import get_session
from app.services.staff_service import get_staff_by_telegram_id, link_telegram_account
from app.bot_business.keyboards.biz_kb import owner_main_menu, staff_main_menu

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    """Welcome the user and route them based on their role."""
    user_id = message.from_user.id

    # 1. Check if Owner
    if user_id == settings.admin_telegram_id:
        await message.answer(
            f"👋 Welcome Owner!\n\nUse the menu below to manage your businesses:",
            reply_markup=owner_main_menu(),
        )
        return

    # 2. Check if Staff
    async with get_session() as session:
        staff = await get_staff_by_telegram_id(session, user_id)

    if staff:
        await message.answer(
            f"💈 Welcome back, {staff.name}!\n\nHere's your staff panel:",
            reply_markup=staff_main_menu(),
        )
        return

    # 3. Unlinked user
    await message.answer(
        "👋 Welcome to the Staff Bot!\n\n"
        "It looks like your account is not linked to a staff profile yet.\n\n"
        "To link your account, ask your owner for a link code and send it like this:\n"
        "`/link BARBER-1234`",
        parse_mode="Markdown",
    )


@router.message(Command("link"))
async def cmd_link(message: Message) -> None:
    """Link a staff profile using a code."""
    args = message.text.split(" ")
    if len(args) < 2:
        await message.answer("❌ Please provide a code. Example: `/link BARBER-1234`", parse_mode="Markdown")
        return

    code = args[1].strip().upper()
    user_id = message.from_user.id

    async with get_session() as session:
        staff = await link_telegram_account(session, code, user_id)

    if not staff:
        await message.answer("❌ Invalid or expired link code.")
        return

    await message.answer(
        f"✅ Successfully linked to **{staff.name}**!\n\nWelcome to your staff panel.",
        reply_markup=staff_main_menu(),
        parse_mode="Markdown",
    )
