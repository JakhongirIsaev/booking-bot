"""
Start handler — bot entry point with registration flow.

Handles:
- /start — if new user: language → name → phone → main menu
- /start — if existing user: show main menu in their language
- Main menu callback
- Language change
"""

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.config.settings import settings
from app.database.session import get_session
from app.i18n import t
from app.services.client_service import (
    get_client_by_telegram_id,
    get_or_create_client,
    update_client_language,
    update_client_name,
    update_client_phone,
)
from app.bot.states import RegistrationStates
from app.bot.keyboards.client_kb import (
    main_menu_keyboard,
    language_keyboard,
)

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext) -> None:
    """
    Handle /start command.

    - New user → start registration (choose language)
    - Existing user → show main menu in their language
    """
    await state.clear()

    async with get_session() as session:
        client = await get_client_by_telegram_id(session, message.from_user.id)

    if client is not None:
        # Existing user — show main menu
        lang = client.language
        await message.answer(
            t("welcome_back", lang, business=settings.business_name),
            reply_markup=main_menu_keyboard(lang),
            parse_mode="HTML",
        )
    else:
        # New user — start registration with language selection
        await state.set_state(RegistrationStates.choosing_language)
        await message.answer(
            "🌐 Выберите язык / Tilni tanlang / Choose your language:",
            reply_markup=language_keyboard(),
            parse_mode="HTML",
        )


# ─── Registration: Language Selected ────────────────────────────────

@router.callback_query(RegistrationStates.choosing_language, F.data.startswith("lang:"))
async def reg_language_chosen(callback: CallbackQuery, state: FSMContext) -> None:
    """Language selected — ask for name."""
    lang = callback.data.split(":")[1]
    await state.update_data(language=lang)

    # Create a placeholder client record
    async with get_session() as session:
        await get_or_create_client(
            session, callback.from_user.id,
            name=callback.from_user.full_name or "User",
            language=lang,
        )

    await state.set_state(RegistrationStates.entering_name)
    await callback.message.edit_text(
        t("ask_name", lang),
        parse_mode="HTML",
    )
    await callback.answer()


# ─── Registration: Name Entered ─────────────────────────────────────

@router.message(RegistrationStates.entering_name)
async def reg_name_entered(message: Message, state: FSMContext) -> None:
    """User typed their name — ask for phone."""
    name = message.text.strip()
    if not name or len(name) < 2:
        data = await state.get_data()
        lang = data.get("language", "ru")
        await message.answer(t("ask_name", lang), parse_mode="HTML")
        return

    data = await state.get_data()
    lang = data.get("language", "ru")
    await state.update_data(name=name)

    # Save name to DB
    async with get_session() as session:
        await update_client_name(session, message.from_user.id, name)

    await state.set_state(RegistrationStates.entering_phone)
    await message.answer(
        t("ask_phone", lang),
        parse_mode="HTML",
    )


# ─── Registration: Phone Entered ────────────────────────────────────

@router.message(RegistrationStates.entering_phone)
async def reg_phone_entered(message: Message, state: FSMContext) -> None:
    """User typed phone number — complete registration."""
    phone = message.text.strip()
    data = await state.get_data()
    lang = data.get("language", "ru")
    name = data.get("name", "User")

    # Validate phone — must be at least 9 digits
    digits_only = ''.join(c for c in phone if c.isdigit())
    if len(digits_only) < 9:
        await message.answer(t("ask_phone", lang), parse_mode="HTML")
        return

    # Save phone to DB
    async with get_session() as session:
        await update_client_phone(session, message.from_user.id, phone)

    await state.clear()
    await message.answer(
        t("registration_complete", lang, business=settings.business_name, name=name),
        reply_markup=main_menu_keyboard(lang),
        parse_mode="HTML",
    )





# ─── Main Menu ──────────────────────────────────────────────────────

@router.callback_query(F.data == "main_menu")
async def callback_main_menu(callback: CallbackQuery, state: FSMContext) -> None:
    """Return to main menu from anywhere."""
    await state.clear()

    async with get_session() as session:
        client = await get_client_by_telegram_id(session, callback.from_user.id)
    lang = client.language if client else "ru"

    await callback.message.edit_text(
        t("welcome_back", lang, business=settings.business_name),
        reply_markup=main_menu_keyboard(lang),
        parse_mode="HTML",
    )
    await callback.answer()


# ─── Change Language ────────────────────────────────────────────────

@router.callback_query(F.data == "change_lang")
async def change_language(callback: CallbackQuery, state: FSMContext) -> None:
    """Show language selection for existing users."""
    await callback.message.edit_text(
        "🌐 Выберите язык / Tilni tanlang / Choose your language:",
        reply_markup=language_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("lang:"))
async def update_language(callback: CallbackQuery, state: FSMContext) -> None:
    """Update language for existing user (not in registration)."""
    lang = callback.data.split(":")[1]

    async with get_session() as session:
        await update_client_language(session, callback.from_user.id, lang)

    await callback.message.edit_text(
        t("welcome_back", lang, business=settings.business_name),
        reply_markup=main_menu_keyboard(lang),
        parse_mode="HTML",
    )
    await callback.answer()
