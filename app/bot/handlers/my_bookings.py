"""
My Bookings handler — view and cancel existing bookings.

Allows clients to:
- View their upcoming bookings
- Cancel a specific booking
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from app.database.session import get_session
from app.services.booking_service import get_client_bookings, cancel_booking
from app.services.client_service import get_client_by_telegram_id
from app.bot.keyboards.client_kb import my_bookings_keyboard, main_menu_keyboard

router = Router()


@router.callback_query(F.data == "my_bookings")
async def show_my_bookings(callback: CallbackQuery, state: FSMContext) -> None:
    """Show the client's upcoming bookings."""
    await state.clear()

    async with get_session() as session:
        client = await get_client_by_telegram_id(
            session=session,
            telegram_id=callback.from_user.id,
        )

        if client is None:
            await callback.message.edit_text(
                "📋 You have no bookings yet.\n\n"
                "Tap <b>Book Appointment</b> to get started!",
                reply_markup=main_menu_keyboard(),
                parse_mode="HTML",
            )
            await callback.answer()
            return

        bookings = await get_client_bookings(
            session=session,
            client_id=client.id,
        )

    if not bookings:
        await callback.message.edit_text(
            "📋 <b>No upcoming bookings.</b>\n\n"
            "Tap <b>Book Appointment</b> to schedule one!",
            reply_markup=main_menu_keyboard(),
            parse_mode="HTML",
        )
        await callback.answer()
        return

    await callback.message.edit_text(
        f"📋 <b>Your Upcoming Bookings:</b>\n\n"
        f"You have <b>{len(bookings)}</b> upcoming appointment(s):",
        reply_markup=my_bookings_keyboard(bookings),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("cancel_booking:"))
async def cancel_booking_handler(callback: CallbackQuery, state: FSMContext) -> None:
    """Cancel a specific booking."""
    booking_id = callback.data.split(":")[1]

    async with get_session() as session:
        client = await get_client_by_telegram_id(
            session=session,
            telegram_id=callback.from_user.id,
        )

        if client is None:
            await callback.answer("❌ Error: Client not found.", show_alert=True)
            return

        success = await cancel_booking(
            session=session,
            booking_id=booking_id,
            client_id=client.id,
        )

    if success:
        await callback.answer("✅ Booking cancelled!", show_alert=True)
        # Refresh the bookings list
        await show_my_bookings(callback, state)
    else:
        await callback.answer(
            "❌ Could not cancel booking. It may already be cancelled.",
            show_alert=True,
        )
