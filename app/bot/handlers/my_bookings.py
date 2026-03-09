"""
My Bookings handler — view and cancel existing bookings (with i18n).
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from app.database.session import get_session
from app.i18n import t
from app.services.booking_service import get_client_bookings, cancel_booking
from app.services.client_service import get_client_by_telegram_id
from app.bot.keyboards.client_kb import my_bookings_keyboard, main_menu_keyboard

router = Router()


@router.callback_query(F.data == "my_bookings")
async def show_my_bookings(callback: CallbackQuery, state: FSMContext) -> None:
    """Show the client's upcoming bookings."""
    await state.clear()

    async with get_session() as session:
        client = await get_client_by_telegram_id(session, callback.from_user.id)

        if client is None:
            await callback.message.edit_text(
                t("no_bookings_yet", "ru"),
                reply_markup=main_menu_keyboard("ru"),
                parse_mode="HTML",
            )
            await callback.answer()
            return

        lang = client.language
        bookings = await get_client_bookings(session, client.id)

    if not bookings:
        await callback.message.edit_text(
            t("no_upcoming", lang),
            reply_markup=main_menu_keyboard(lang),
            parse_mode="HTML",
        )
        await callback.answer()
        return

    await callback.message.edit_text(
        t("your_bookings", lang, count=len(bookings)),
        reply_markup=my_bookings_keyboard(bookings, lang),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("cancel_booking:"))
async def cancel_booking_handler(callback: CallbackQuery, state: FSMContext) -> None:
    """Cancel a specific booking."""
    booking_id = callback.data.split(":")[1]

    async with get_session() as session:
        client = await get_client_by_telegram_id(session, callback.from_user.id)

        if client is None:
            await callback.answer("❌", show_alert=True)
            return

        lang = client.language
        success = await cancel_booking(session, booking_id, client.id)

    if success:
        await callback.answer(t("booking_cancelled_ok", lang), show_alert=True)
        await show_my_bookings(callback, state)
    else:
        await callback.answer(t("booking_cancel_fail", lang), show_alert=True)
