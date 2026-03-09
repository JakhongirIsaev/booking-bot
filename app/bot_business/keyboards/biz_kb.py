"""
Business bot inline keyboards for Owners and Staff.
"""

import uuid
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def owner_main_menu() -> InlineKeyboardMarkup:
    """Main menu for Business Owners."""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🏢 My Shops", callback_data="owner:shops"))
    builder.row(InlineKeyboardButton(text="👥 My Staff", callback_data="owner:staff"))
    builder.row(InlineKeyboardButton(text="📋 All Bookings", callback_data="owner:bookings"))
    return builder.as_markup()


def owner_staff_list(staff_list: list) -> InlineKeyboardMarkup:
    """List of staff members to generate link codes."""
    builder = InlineKeyboardBuilder()
    for staff in staff_list:
        status = "✅ Linked" if staff.telegram_id else "🔗 Generate Link"
        builder.row(
            InlineKeyboardButton(
                text=f"{staff.name} ({status})",
                callback_data=f"owner:link_staff:{staff.id}"
            )
        )
    builder.row(InlineKeyboardButton(text="⬅️ Back", callback_data="owner:main_menu"))
    return builder.as_markup()


def staff_main_menu() -> InlineKeyboardMarkup:
    """Main menu for Staff members."""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="📅 Today's Schedule", callback_data="staff:today"))
    builder.row(InlineKeyboardButton(text="🔜 Tomorrow's Schedule", callback_data="staff:tomorrow"))
    return builder.as_markup()


def back_to_staff_menu() -> InlineKeyboardMarkup:
    """Simple back button for staff."""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="⬅️ Back to Menu", callback_data="staff:main_menu"))
    return builder.as_markup()


def back_to_owner_menu() -> InlineKeyboardMarkup:
    """Simple back button for owners."""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="⬅️ Back to Menu", callback_data="owner:main_menu"))
    return builder.as_markup()
