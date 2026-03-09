"""
Business bot inline keyboards for Owners and Staff.
"""

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.i18n import t


def owner_main_menu(lang: str = "ru") -> InlineKeyboardMarkup:
    """Main menu for Business Owners."""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=t("btn_my_shops", lang), callback_data="owner:shops"))
    builder.row(InlineKeyboardButton(text=t("btn_my_staff", lang), callback_data="owner:staff"))
    builder.row(InlineKeyboardButton(text=t("btn_all_bookings", lang), callback_data="owner:bookings"))
    builder.row(InlineKeyboardButton(text=t("btn_change_lang", lang), callback_data="biz_lang_picker"))
    return builder.as_markup()


def owner_bookings_submenu(lang: str = "ru") -> InlineKeyboardMarkup:
    """Submenu for viewing bookings."""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=t("btn_today_bookings", lang), callback_data="owner:bookings_today"))
    builder.row(InlineKeyboardButton(text=t("btn_upcoming_bookings", lang), callback_data="owner:bookings_upcoming"))
    builder.row(InlineKeyboardButton(text=t("btn_back_menu", lang), callback_data="owner:main_menu"))
    return builder.as_markup()


def owner_staff_list(staff_list: list, lang: str = "ru") -> InlineKeyboardMarkup:
    """List of staff members to generate link codes."""
    builder = InlineKeyboardBuilder()
    for staff in staff_list:
        status = t("status_linked", lang) if staff.telegram_id else t("status_unlinked", lang)
        builder.row(
            InlineKeyboardButton(
                text=f"{staff.name} ({status})",
                callback_data=f"owner:link_staff:{staff.id}"
            )
        )
    builder.row(InlineKeyboardButton(text=t("btn_back_menu", lang), callback_data="owner:main_menu"))
    return builder.as_markup()


def staff_main_menu(lang: str = "ru") -> InlineKeyboardMarkup:
    """Main menu for Staff members."""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=t("btn_today", lang), callback_data="staff:today"))
    builder.row(InlineKeyboardButton(text=t("btn_tomorrow", lang), callback_data="staff:tomorrow"))
    # Also allow staff to switch language easily
    builder.row(InlineKeyboardButton(text=t("btn_change_lang", lang), callback_data="biz_lang_picker"))
    return builder.as_markup()


def back_to_staff_menu(lang: str = "ru") -> InlineKeyboardMarkup:
    """Simple back button for staff."""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=t("btn_back_menu", lang), callback_data="staff:main_menu"))
    return builder.as_markup()


def back_to_owner_menu(lang: str = "ru") -> InlineKeyboardMarkup:
    """Simple back button for owners."""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=t("btn_back_menu", lang), callback_data="owner:main_menu"))
    return builder.as_markup()


def lang_picker_kb() -> InlineKeyboardMarkup:
    """Keyboard for selecting language."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🇷🇺 Русский", callback_data="biz_lang:ru"),
        InlineKeyboardButton(text="🇺🇿 O'zbek", callback_data="biz_lang:uz"),
        InlineKeyboardButton(text="🇬🇧 English", callback_data="biz_lang:en")
    )
    return builder.as_markup()
