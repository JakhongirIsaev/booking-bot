"""
Client-side inline keyboards for registration, browsing, and booking flows.

All keyboards accept a `lang` parameter for multi-language support.
"""

from datetime import date, datetime
from typing import List, Tuple

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.i18n import t, get_day_names


def language_keyboard() -> InlineKeyboardMarkup:
    """Language selection keyboard."""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru"))
    builder.row(InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="lang:uz"))
    builder.row(InlineKeyboardButton(text="🇬🇧 English", callback_data="lang:en"))
    return builder.as_markup()


def main_menu_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    """Main menu: Book / My Bookings / Change Language."""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=t("btn_book", lang), callback_data="book_start"))
    builder.row(InlineKeyboardButton(text=t("btn_my_bookings", lang), callback_data="my_bookings"))
    builder.row(InlineKeyboardButton(text=t("btn_change_lang", lang), callback_data="change_lang"))
    return builder.as_markup()


def category_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    """Business category selection (barbershop / nails)."""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=t("cat_barbershop", lang), callback_data="cat:barbershop"))
    builder.row(InlineKeyboardButton(text=t("cat_nails", lang), callback_data="cat:nails"))
    builder.row(InlineKeyboardButton(text=t("btn_main_menu", lang), callback_data="main_menu"))
    return builder.as_markup()


def shops_keyboard(shops: list, lang: str = "ru") -> InlineKeyboardMarkup:
    """Shop list for a given category."""
    builder = InlineKeyboardBuilder()
    for shop in shops:
        builder.row(
            InlineKeyboardButton(
                text=f"🏢 {shop.name}",
                callback_data=f"shop:{shop.id}",
            )
        )
    builder.row(
        InlineKeyboardButton(text=t("btn_back", lang), callback_data="book_start"),
        InlineKeyboardButton(text=t("btn_main_menu", lang), callback_data="main_menu"),
    )
    return builder.as_markup()


def shop_info_keyboard(shop_id: str, lang: str = "ru") -> InlineKeyboardMarkup:
    """Shop info card with 'Book Here' button."""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=t("btn_book_here", lang), callback_data=f"book_at:{shop_id}"))
    builder.row(
        InlineKeyboardButton(text=t("btn_back", lang), callback_data="back_to_shops"),
        InlineKeyboardButton(text=t("btn_main_menu", lang), callback_data="main_menu"),
    )
    return builder.as_markup()


def services_keyboard(services: list, lang: str = "ru") -> InlineKeyboardMarkup:
    """Service selection keyboard with localized names and prices."""
    builder = InlineKeyboardBuilder()
    currency = t("currency", lang)
    for service in services:
        name = service.get_name(lang)
        price_formatted = f"{int(service.price):,}".replace(",", " ")
        builder.row(
            InlineKeyboardButton(
                text=f"{name} — {price_formatted} {currency}",
                callback_data=f"service:{service.id}",
            )
        )
    builder.row(
        InlineKeyboardButton(text=t("btn_back", lang), callback_data="back_to_shop_info"),
        InlineKeyboardButton(text=t("btn_cancel", lang), callback_data="cancel_booking_flow"),
    )
    return builder.as_markup()


def staff_keyboard(staff_list: list, lang: str = "ru") -> InlineKeyboardMarkup:
    """Staff (barber/master) selection keyboard."""
    builder = InlineKeyboardBuilder()
    for staff in staff_list:
        builder.row(
            InlineKeyboardButton(
                text=f"💈 {staff.name}",
                callback_data=f"staff:{staff.id}",
            )
        )
    builder.row(
        InlineKeyboardButton(text=t("btn_back", lang), callback_data="back_to_services"),
        InlineKeyboardButton(text=t("btn_cancel", lang), callback_data="cancel_booking_flow"),
    )
    return builder.as_markup()


def dates_keyboard(dates: List[date], lang: str = "ru") -> InlineKeyboardMarkup:
    """Date picker with localized day names."""
    builder = InlineKeyboardBuilder()
    day_names = get_day_names(lang)
    today_label = t("today", lang)

    for d in dates:
        day_name = day_names.get(d.weekday(), "")
        label = f"{day_name}, {d.strftime('%d.%m')}"
        if d == datetime.now().date():
            label = f"{today_label} ({d.strftime('%d.%m')})"
        builder.row(InlineKeyboardButton(text=label, callback_data=f"date:{d.isoformat()}"))

    builder.row(
        InlineKeyboardButton(text=t("btn_back", lang), callback_data="back_to_staff"),
        InlineKeyboardButton(text=t("btn_cancel", lang), callback_data="cancel_booking_flow"),
    )
    return builder.as_markup()


def time_slots_keyboard(slots: List[Tuple[datetime, datetime]], lang: str = "ru") -> InlineKeyboardMarkup:
    """Time slot grid in 3 columns."""
    builder = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(text=f"🕐 {s.strftime('%H:%M')}", callback_data=f"time:{s.isoformat()}")
        for s, _ in slots
    ]
    for i in range(0, len(buttons), 3):
        builder.row(*buttons[i : i + 3])
    builder.row(
        InlineKeyboardButton(text=t("btn_back", lang), callback_data="back_to_date"),
        InlineKeyboardButton(text=t("btn_cancel", lang), callback_data="cancel_booking_flow"),
    )
    return builder.as_markup()


def confirm_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    """Confirm / Back / Cancel."""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=t("btn_confirm", lang), callback_data="confirm_yes"))
    builder.row(
        InlineKeyboardButton(text=t("btn_back", lang), callback_data="back_to_time"),
        InlineKeyboardButton(text=t("btn_cancel", lang), callback_data="cancel_booking_flow"),
    )
    return builder.as_markup()


def my_bookings_keyboard(bookings: list, lang: str = "ru") -> InlineKeyboardMarkup:
    """My bookings list with cancel buttons."""
    builder = InlineKeyboardBuilder()
    for booking in bookings:
        time_str = booking.start_time.strftime("%d.%m %H:%M")
        service_name = booking.service.get_name(lang) if booking.service else "—"
        staff_name = booking.staff.name if booking.staff else "—"
        builder.row(InlineKeyboardButton(
            text=f"📅 {time_str} | {service_name} | {staff_name}",
            callback_data=f"view_booking:{booking.id}",
        ))
        builder.row(InlineKeyboardButton(
            text=t("btn_cancel_booking", lang),
            callback_data=f"cancel_booking:{booking.id}",
        ))
    builder.row(InlineKeyboardButton(text=t("btn_main_menu", lang), callback_data="main_menu"))
    return builder.as_markup()


def no_slots_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    """No slots — choose another date."""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=t("btn_another_date", lang), callback_data="back_to_date"))
    builder.row(InlineKeyboardButton(text=t("btn_main_menu", lang), callback_data="main_menu"))
    return builder.as_markup()
