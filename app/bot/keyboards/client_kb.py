"""
Client-side inline keyboards for the booking flow.

Builds dynamic inline keyboards for each step of the booking process:
- Service selection
- Staff (barber) selection
- Date picker (next 7 days)
- Time slot grid
- Booking confirmation
- My bookings list with cancel buttons
"""

from datetime import date, datetime
from typing import List, Tuple
import uuid

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_menu_keyboard() -> InlineKeyboardMarkup:
    """Main menu: Book Appointment / My Bookings."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="📅 Book Appointment",
            callback_data="book_start",
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="📋 My Bookings",
            callback_data="my_bookings",
        )
    )
    return builder.as_markup()


def services_keyboard(services: list) -> InlineKeyboardMarkup:
    """
    Service selection keyboard.

    Each button shows: service name + price.
    Callback data: service:{service_id}
    """
    builder = InlineKeyboardBuilder()
    for service in services:
        price_formatted = f"{int(service.price):,}".replace(",", " ")
        builder.row(
            InlineKeyboardButton(
                text=f"{service.name} — {price_formatted} сум",
                callback_data=f"service:{service.id}",
            )
        )
    builder.row(
        InlineKeyboardButton(text="❌ Cancel", callback_data="cancel_booking_flow")
    )
    return builder.as_markup()


def staff_keyboard(staff_list: list) -> InlineKeyboardMarkup:
    """
    Staff (barber) selection keyboard.

    Each button shows: staff name.
    Callback data: staff:{staff_id}
    """
    builder = InlineKeyboardBuilder()
    for staff in staff_list:
        builder.row(
            InlineKeyboardButton(
                text=f"💈 {staff.name}",
                callback_data=f"staff:{staff.id}",
            )
        )
    builder.row(
        InlineKeyboardButton(text="⬅️ Back", callback_data="book_start"),
        InlineKeyboardButton(text="❌ Cancel", callback_data="cancel_booking_flow"),
    )
    return builder.as_markup()


def dates_keyboard(dates: List[date]) -> InlineKeyboardMarkup:
    """
    Date picker keyboard.

    Shows next 7 days with day name and date.
    Callback data: date:YYYY-MM-DD
    """
    builder = InlineKeyboardBuilder()

    day_names = {
        0: "Mon", 1: "Tue", 2: "Wed", 3: "Thu",
        4: "Fri", 5: "Sat", 6: "Sun",
    }
    day_names_ru = {
        0: "Пн", 1: "Вт", 2: "Ср", 3: "Чт",
        4: "Пт", 5: "Сб", 6: "Вс",
    }

    for d in dates:
        day_name = day_names_ru.get(d.weekday(), "")
        label = f"{day_name}, {d.strftime('%d.%m')}"

        # Mark today
        from datetime import datetime as dt
        if d == dt.now().date():
            label = f"📌 Today ({d.strftime('%d.%m')})"

        builder.row(
            InlineKeyboardButton(
                text=label,
                callback_data=f"date:{d.isoformat()}",
            )
        )

    builder.row(
        InlineKeyboardButton(text="⬅️ Back", callback_data="back_to_staff"),
        InlineKeyboardButton(text="❌ Cancel", callback_data="cancel_booking_flow"),
    )
    return builder.as_markup()


def time_slots_keyboard(
    slots: List[Tuple[datetime, datetime]],
) -> InlineKeyboardMarkup:
    """
    Time slot grid keyboard.

    Shows available time slots in a 3-column grid.
    Callback data: time:{ISO datetime}
    """
    builder = InlineKeyboardBuilder()

    buttons = []
    for start, end in slots:
        label = start.strftime("%H:%M")
        buttons.append(
            InlineKeyboardButton(
                text=f"🕐 {label}",
                callback_data=f"time:{start.isoformat()}",
            )
        )

    # Arrange in rows of 3
    for i in range(0, len(buttons), 3):
        row = buttons[i : i + 3]
        builder.row(*row)

    builder.row(
        InlineKeyboardButton(text="⬅️ Back", callback_data="back_to_date"),
        InlineKeyboardButton(text="❌ Cancel", callback_data="cancel_booking_flow"),
    )
    return builder.as_markup()


def confirm_keyboard() -> InlineKeyboardMarkup:
    """Confirmation keyboard: Confirm / Cancel."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="✅ Confirm Booking",
            callback_data="confirm_yes",
        )
    )
    builder.row(
        InlineKeyboardButton(text="⬅️ Back", callback_data="back_to_time"),
        InlineKeyboardButton(text="❌ Cancel", callback_data="cancel_booking_flow"),
    )
    return builder.as_markup()


def my_bookings_keyboard(bookings: list) -> InlineKeyboardMarkup:
    """
    My bookings list with cancel buttons.

    Each booking shows: date, time, service, staff.
    Cancel button for each booking.
    """
    builder = InlineKeyboardBuilder()

    for booking in bookings:
        time_str = booking.start_time.strftime("%d.%m %H:%M")
        service_name = booking.service.name if booking.service else "Service"
        staff_name = booking.staff.name if booking.staff else "Staff"

        builder.row(
            InlineKeyboardButton(
                text=f"📅 {time_str} | {service_name} | {staff_name}",
                callback_data=f"view_booking:{booking.id}",
            )
        )
        builder.row(
            InlineKeyboardButton(
                text=f"❌ Cancel this booking",
                callback_data=f"cancel_booking:{booking.id}",
            )
        )

    builder.row(
        InlineKeyboardButton(text="🏠 Main Menu", callback_data="main_menu"),
    )
    return builder.as_markup()


def no_slots_keyboard() -> InlineKeyboardMarkup:
    """Shown when no time slots are available."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="⬅️ Choose Another Date", callback_data="back_to_date"),
    )
    builder.row(
        InlineKeyboardButton(text="🏠 Main Menu", callback_data="main_menu"),
    )
    return builder.as_markup()
