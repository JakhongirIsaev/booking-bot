"""
Start handler — bot entry point.

Handles:
- /start command — greet user, auto-register, show main menu
- Main menu callback — return to main menu from anywhere

This is the first handler that runs when a user interacts with the bot.
It auto-registers the user as a client (get-or-create pattern).
"""

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.config.settings import settings
from app.database.session import get_session
from app.services.client_service import get_or_create_client
from app.bot.keyboards.client_kb import main_menu_keyboard

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext) -> None:
    """
    Handle /start command.

    1. Register/update the client in the database
    2. Clear any active FSM state
    3. Show welcome message with main menu
    """
    # Clear any ongoing booking flow
    await state.clear()

    # Auto-register client
    async with get_session() as session:
        user = message.from_user
        await get_or_create_client(
            session=session,
            telegram_id=user.id,
            name=user.full_name or "Unknown",
        )

    # Welcome message
    welcome_text = (
        f"👋 Welcome to <b>{settings.business_name}</b>!\n\n"
        f"I can help you book an appointment.\n"
        f"Choose an option below:"
    )

    await message.answer(
        welcome_text,
        reply_markup=main_menu_keyboard(),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "main_menu")
async def callback_main_menu(callback: CallbackQuery, state: FSMContext) -> None:
    """Return to main menu from anywhere."""
    await state.clear()

    welcome_text = (
        f"👋 <b>{settings.business_name}</b>\n\n"
        f"Choose an option:"
    )

    await callback.message.edit_text(
        welcome_text,
        reply_markup=main_menu_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer()
