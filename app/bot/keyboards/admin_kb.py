"""
Admin inline keyboards.

Provides keyboards for the admin interface:
- Admin menu
- Booking list actions
"""

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def admin_menu_keyboard() -> InlineKeyboardMarkup:
    """Admin main menu keyboard."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="📅 Today's Bookings",
            callback_data="admin_today",
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="📋 All Upcoming Bookings",
            callback_data="admin_upcoming",
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="📊 Statistics",
            callback_data="admin_stats",
        )
    )
    return builder.as_markup()
