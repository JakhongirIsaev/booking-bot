"""
Internationalization (i18n) — translations for Russian, Uzbek, English.

This module provides all bot text in three languages.
Each text key maps to a dict of {lang_code: translated_string}.

Usage:
    from app.i18n import t
    text = t("welcome", lang="ru")  # Returns Russian translation

Language codes:
    "ru" — Russian (default)
    "uz" — Uzbek
    "en" — English
"""

from app.config.settings import settings

TRANSLATIONS = {
    # ─── Language selection ───────────────────────────────────────
    "choose_language": {
        "ru": "🌐 Выберите язык:",
        "uz": "🌐 Tilni tanlang:",
        "en": "🌐 Choose your language:",
    },

    # ─── Registration ────────────────────────────────────────────
    "ask_name": {
        "ru": "👋 Добро пожаловать!\n\nПожалуйста, введите ваше имя:",
        "uz": "👋 Xush kelibsiz!\n\nIltimos, ismingizni kiriting:",
        "en": "👋 Welcome!\n\nPlease enter your name:",
    },
    "ask_phone": {
        "ru": "📱 Введите ваш номер телефона\n(или нажмите «Пропустить»):",
        "uz": "📱 Telefon raqamingizni kiriting\n(yoki «O'tkazib yuborish» tugmasini bosing):",
        "en": "📱 Enter your phone number\n(or press «Skip»):",
    },
    "skip": {
        "ru": "⏭ Пропустить",
        "uz": "⏭ O'tkazib yuborish",
        "en": "⏭ Skip",
    },
    "registration_complete": {
        "ru": "✅ Регистрация завершена!\n\nДобро пожаловать в <b>{business}</b>, <b>{name}</b>!",
        "uz": "✅ Ro'yxatdan o'tish yakunlandi!\n\n<b>{business}</b>ga xush kelibsiz, <b>{name}</b>!",
        "en": "✅ Registration complete!\n\nWelcome to <b>{business}</b>, <b>{name}</b>!",
    },

    # ─── Main menu ───────────────────────────────────────────────
    "welcome_back": {
        "ru": "👋 <b>{business}</b>\n\nВыберите действие:",
        "uz": "👋 <b>{business}</b>\n\nAmalni tanlang:",
        "en": "👋 <b>{business}</b>\n\nChoose an option:",
    },
    "btn_book": {
        "ru": "📅 Записаться",
        "uz": "📅 Yozilish",
        "en": "📅 Book Appointment",
    },
    "btn_my_bookings": {
        "ru": "📋 Мои записи",
        "uz": "📋 Mening yozuvlarim",
        "en": "📋 My Bookings",
    },
    "btn_change_lang": {
        "ru": "🌐 Сменить язык",
        "uz": "🌐 Tilni o'zgartirish",
        "en": "🌐 Change Language",
    },

    # ─── Booking flow ────────────────────────────────────────────
    "choose_service": {
        "ru": "💈 <b>Выберите услугу:</b>",
        "uz": "💈 <b>Xizmatni tanlang:</b>",
        "en": "💈 <b>Choose a service:</b>",
    },
    "no_services": {
        "ru": "❌ Услуги временно недоступны.",
        "uz": "❌ Xizmatlar vaqtincha mavjud emas.",
        "en": "❌ No services available at the moment.",
    },
    "service_selected": {
        "ru": "✅ Услуга: <b>{service}</b>\n\n👤 <b>Выберите мастера:</b>",
        "uz": "✅ Xizmat: <b>{service}</b>\n\n👤 <b>Ustani tanlang:</b>",
        "en": "✅ Service: <b>{service}</b>\n\n👤 <b>Choose a barber:</b>",
    },
    "no_staff": {
        "ru": "❌ Мастера временно недоступны.",
        "uz": "❌ Ustalar vaqtincha mavjud emas.",
        "en": "❌ No staff available at the moment.",
    },
    "staff_selected": {
        "ru": "👤 Мастер: <b>{staff}</b>\n\n📅 <b>Выберите дату:</b>",
        "uz": "👤 Usta: <b>{staff}</b>\n\n📅 <b>Sanani tanlang:</b>",
        "en": "👤 Barber: <b>{staff}</b>\n\n📅 <b>Choose a date:</b>",
    },
    "choose_time": {
        "ru": "📅 Дата: <b>{date}</b>\n\n🕐 <b>Выберите время:</b>",
        "uz": "📅 Sana: <b>{date}</b>\n\n🕐 <b>Vaqtni tanlang:</b>",
        "en": "📅 Date: <b>{date}</b>\n\n🕐 <b>Choose a time:</b>",
    },
    "no_slots": {
        "ru": "😔 <b>Нет свободных окон</b> на {date}.\n\nПопробуйте другую дату.",
        "uz": "😔 {date} da <b>bo'sh joy yo'q</b>.\n\nBoshqa sanani tanlang.",
        "en": "😔 <b>No available slots</b> on {date}.\n\nTry a different date.",
    },
    "no_slots_remaining": {
        "ru": "😔 <b>Свободных окон не осталось.</b>\n\nПопробуйте другую дату.",
        "uz": "😔 <b>Bo'sh joy qolmadi.</b>\n\nBoshqa sanani tanlang.",
        "en": "😔 <b>No available slots</b> remaining.\n\nTry a different date.",
    },

    # ─── Booking summary ─────────────────────────────────────────
    "booking_summary": {
        "ru": (
            "📋 <b>Подтверждение записи</b>\n\n"
            "💈 Услуга: <b>{service}</b>\n"
            "👤 Мастер: <b>{staff}</b>\n"
            "📅 Дата: <b>{date}</b>\n"
            "🕐 Время: <b>{time}</b>\n"
            "⏱ Длительность: <b>{duration}</b>\n"
            "💰 Цена: <b>{price} сум</b>\n\n"
            "Подтвердить запись?"
        ),
        "uz": (
            "📋 <b>Yozuvni tasdiqlash</b>\n\n"
            "💈 Xizmat: <b>{service}</b>\n"
            "👤 Usta: <b>{staff}</b>\n"
            "📅 Sana: <b>{date}</b>\n"
            "🕐 Vaqt: <b>{time}</b>\n"
            "⏱ Davomiyligi: <b>{duration}</b>\n"
            "💰 Narx: <b>{price} so'm</b>\n\n"
            "Yozuvni tasdiqlaysizmi?"
        ),
        "en": (
            "📋 <b>Booking Summary</b>\n\n"
            "💈 Service: <b>{service}</b>\n"
            "👤 Barber: <b>{staff}</b>\n"
            "📅 Date: <b>{date}</b>\n"
            "🕐 Time: <b>{time}</b>\n"
            "⏱ Duration: <b>{duration}</b>\n"
            "💰 Price: <b>{price} сум</b>\n\n"
            "Confirm your booking?"
        ),
    },
    "booking_confirmed": {
        "ru": (
            "✅ <b>Запись подтверждена!</b>\n\n"
            "💈 Услуга: <b>{service}</b>\n"
            "👤 Мастер: <b>{staff}</b>\n"
            "📅 Дата: <b>{date}</b>\n"
            "🕐 Время: <b>{time}</b>\n\n"
            "Ждём вас в <b>{business}</b>! 💈"
        ),
        "uz": (
            "✅ <b>Yozuv tasdiqlandi!</b>\n\n"
            "💈 Xizmat: <b>{service}</b>\n"
            "👤 Usta: <b>{staff}</b>\n"
            "📅 Sana: <b>{date}</b>\n"
            "🕐 Vaqt: <b>{time}</b>\n\n"
            "<b>{business}</b>da kutamiz! 💈"
        ),
        "en": (
            "✅ <b>Booking Confirmed!</b>\n\n"
            "💈 Service: <b>{service}</b>\n"
            "👤 Barber: <b>{staff}</b>\n"
            "📅 Date: <b>{date}</b>\n"
            "🕐 Time: <b>{time}</b>\n\n"
            "See you at <b>{business}</b>! 💈"
        ),
    },
    "slot_taken": {
        "ru": "😔 <b>К сожалению, это время уже занято.</b>\n\nПопробуйте другое время.",
        "uz": "😔 <b>Afsuski, bu vaqt band.</b>\n\nBoshqa vaqtni tanlang.",
        "en": "😔 <b>Sorry, this slot is no longer available.</b>\n\nPlease try again.",
    },
    "booking_cancelled_flow": {
        "ru": "❌ Запись отменена.\n\n👋 <b>{business}</b>\nВыберите действие:",
        "uz": "❌ Yozuv bekor qilindi.\n\n👋 <b>{business}</b>\nAmalni tanlang:",
        "en": "❌ Booking cancelled.\n\n👋 <b>{business}</b>\nChoose an option:",
    },
    "error_business_not_found": {
        "ru": "❌ Ошибка: бизнес не найден.",
        "uz": "❌ Xato: biznes topilmadi.",
        "en": "❌ Error: Business not found. Contact admin.",
    },

    # ─── Buttons ─────────────────────────────────────────────────
    "btn_confirm": {
        "ru": "✅ Подтвердить запись",
        "uz": "✅ Yozuvni tasdiqlash",
        "en": "✅ Confirm Booking",
    },
    "btn_cancel": {
        "ru": "❌ Отмена",
        "uz": "❌ Bekor qilish",
        "en": "❌ Cancel",
    },
    "btn_back": {
        "ru": "⬅️ Назад",
        "uz": "⬅️ Orqaga",
        "en": "⬅️ Back",
    },
    "btn_main_menu": {
        "ru": "🏠 Главное меню",
        "uz": "🏠 Asosiy menyu",
        "en": "🏠 Main Menu",
    },
    "btn_another_date": {
        "ru": "⬅️ Другая дата",
        "uz": "⬅️ Boshqa sana",
        "en": "⬅️ Choose Another Date",
    },
    "btn_cancel_booking": {
        "ru": "❌ Отменить эту запись",
        "uz": "❌ Bu yozuvni bekor qilish",
        "en": "❌ Cancel this booking",
    },

    # ─── My bookings ──────────────────────────────────────────────
    "no_bookings_yet": {
        "ru": "📋 У вас пока нет записей.\n\nНажмите <b>Записаться</b>, чтобы начать!",
        "uz": "📋 Sizda hali yozuvlar yo'q.\n\n<b>Yozilish</b> tugmasini bosing!",
        "en": "📋 You have no bookings yet.\n\nTap <b>Book Appointment</b> to get started!",
    },
    "no_upcoming": {
        "ru": "📋 <b>Нет предстоящих записей.</b>\n\nНажмите <b>Записаться</b>, чтобы записаться!",
        "uz": "📋 <b>Kelgusi yozuvlar yo'q.</b>\n\n<b>Yozilish</b> tugmasini bosing!",
        "en": "📋 <b>No upcoming bookings.</b>\n\nTap <b>Book Appointment</b> to schedule one!",
    },
    "your_bookings": {
        "ru": "📋 <b>Ваши записи:</b>\n\nУ вас <b>{count}</b> предстоящих записей:",
        "uz": "📋 <b>Sizning yozuvlaringiz:</b>\n\nSizda <b>{count}</b> ta kelgusi yozuv bor:",
        "en": "📋 <b>Your Upcoming Bookings:</b>\n\nYou have <b>{count}</b> upcoming appointment(s):",
    },
    "booking_cancelled_ok": {
        "ru": "✅ Запись отменена!",
        "uz": "✅ Yozuv bekor qilindi!",
        "en": "✅ Booking cancelled!",
    },
    "booking_cancel_fail": {
        "ru": "❌ Не удалось отменить запись.",
        "uz": "❌ Yozuvni bekor qilib bo'lmadi.",
        "en": "❌ Could not cancel booking.",
    },

    # ─── Date labels ─────────────────────────────────────────────
    "today": {
        "ru": "📌 Сегодня",
        "uz": "📌 Bugun",
        "en": "📌 Today",
    },
    "day_names": {
        "ru": {0: "Пн", 1: "Вт", 2: "Ср", 3: "Чт", 4: "Пт", 5: "Сб", 6: "Вс"},
        "uz": {0: "Du", 1: "Se", 2: "Ch", 3: "Pa", 4: "Ju", 5: "Sh", 6: "Ya"},
        "en": {0: "Mon", 1: "Tue", 2: "Wed", 3: "Thu", 4: "Fri", 5: "Sat", 6: "Sun"},
    },
    "currency": {
        "ru": "сум",
        "uz": "so'm",
        "en": "сум",
    },
    "minutes": {
        "ru": "мин",
        "uz": "daq",
        "en": "min",
    },
}

DEFAULT_LANG = "ru"


def t(key: str, lang: str = None, **kwargs) -> str:
    """
    Get translated text by key.

    Args:
        key: Translation key (e.g. "welcome_back")
        lang: Language code ("ru", "uz", "en"). Defaults to "ru".
        **kwargs: Format arguments (e.g. business="Demo")

    Returns:
        Translated string with format arguments applied
    """
    if lang is None:
        lang = DEFAULT_LANG

    translations = TRANSLATIONS.get(key, {})
    text = translations.get(lang, translations.get(DEFAULT_LANG, f"[{key}]"))

    if kwargs and isinstance(text, str):
        try:
            text = text.format(**kwargs)
        except (KeyError, IndexError):
            pass

    return text


def get_day_names(lang: str = None) -> dict:
    """Get day name abbreviations for the given language."""
    if lang is None:
        lang = DEFAULT_LANG
    all_days = TRANSLATIONS.get("day_names", {})
    return all_days.get(lang, all_days.get(DEFAULT_LANG, {}))
