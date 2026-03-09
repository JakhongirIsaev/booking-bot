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
        "ru": "📱 Введите ваш номер телефона:",
        "uz": "📱 Telefon raqamingizni kiriting:",
        "en": "📱 Enter your phone number:",
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

    # ─── Categories ──────────────────────────────────────────────
    "choose_category": {
        "ru": "🏢 <b>Выберите тип заведения:</b>",
        "uz": "🏢 <b>Muassasa turini tanlang:</b>",
        "en": "🏢 <b>Choose a business type:</b>",
    },
    "cat_barbershop": {
        "ru": "💈 Барбершоп",
        "uz": "💈 Barbershop",
        "en": "💈 Barbershop",
    },
    "cat_nails": {
        "ru": "💅 Маникюр / Педикюр",
        "uz": "💅 Manikur / Pedikur",
        "en": "💅 Nails",
    },

    # ─── Shop listing ────────────────────────────────────────────
    "choose_shop": {
        "ru": "📍 <b>Выберите заведение:</b>",
        "uz": "📍 <b>Muassasani tanlang:</b>",
        "en": "📍 <b>Choose a shop:</b>",
    },
    "no_shops": {
        "ru": "❌ Заведений в этой категории пока нет.",
        "uz": "❌ Bu kategoriyada muassasalar yo'q.",
        "en": "❌ No shops in this category yet.",
    },
    "shop_info": {
        "ru": "🏢 <b>{name}</b>\n{address}\n📞 {phone}\n\nНажмите кнопку ниже, чтобы записаться:",
        "uz": "🏢 <b>{name}</b>\n{address}\n📞 {phone}\n\nYozilish uchun quyidagi tugmani bosing:",
        "en": "🏢 <b>{name}</b>\n{address}\n📞 {phone}\n\nPress the button below to book:",
    },
    "btn_book_here": {
        "ru": "📅 Записаться сюда",
        "uz": "📅 Bu yerga yozilish",
        "en": "📅 Book Here",
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
    # ─── Business Bot / Staff Panel ──────────────────────────────
    "owner_welcome": {
        "ru": "👋 Добро пожаловать!\n\nИспользуйте меню ниже для управления бизнесом:",
        "uz": "👋 Xush kelibsiz!\n\nBiznesingizni boshqarish uchun menyudan foydalaning:",
        "en": "👋 Welcome Owner!\n\nUse the menu below to manage your businesses:",
    },
    "btn_my_shops": {
        "ru": "🏢 Мои заведения", "uz": "🏢 Mening muassasalarim", "en": "🏢 My Shops",
    },
    "btn_my_staff": {
        "ru": "👥 Мои сотрудники", "uz": "👥 Mening xodimlarim", "en": "👥 My Staff",
    },
    "btn_all_bookings": {
        "ru": "📋 Все записи", "uz": "📋 Barcha yozuvlar", "en": "📋 All Bookings",
    },
    "staff_welcome": {
        "ru": "💈 С возвращением, {name}!\n\nВаша панель сотрудника:",
        "uz": "💈 Qaytganingiz bilan, {name}!\n\nSizning xodim panelingiz:",
        "en": "💈 Welcome back, {name}!\n\nHere's your staff panel:",
    },
    "btn_today": {
        "ru": "📅 Расписание на сегодня", "uz": "📅 Bugungi jadval", "en": "📅 Today's Schedule",
    },
    "btn_tomorrow": {
        "ru": "🔜 Расписание на завтра", "uz": "🔜 Ertangi jadval", "en": "🔜 Tomorrow's Schedule",
    },
    "btn_back_menu": {
        "ru": "⬅️ В меню", "uz": "⬅️ Menyuga", "en": "⬅️ Back to Menu",
    },
    "unlinked_msg": {
        "ru": "👋 Добро пожаловать!\n\nВаш аккаунт еще не привязан к профилю сотрудника.\n\nПопросите у владельца код и отправьте его так:\n`/link КОД`",
        "uz": "👋 Xush kelibsiz!\n\nHisobingiz hali xodim profiliga ulanmagan.\n\nEgadan kod so'rang va xabarnomani bunday yuboring:\n`/link KOD`",
        "en": "👋 Welcome!\n\nIt looks like your account is not linked to a staff profile yet.\n\nTo link your account, ask your owner for a link code and send it like this:\n`/link BARBER-1234`",
    },
    "link_no_code": {
        "ru": "❌ Пожалуйста, укажите код. Пример: `/link BARBER-1234`",
        "uz": "❌ Iltimos, kodni kiriting. Misol: `/link BARBER-1234`",
        "en": "❌ Please provide a code. Example: `/link BARBER-1234`",
    },
    "link_invalid": {
        "ru": "❌ Неверный или просроченный код.",
        "uz": "❌ Noto'g'ri yoki muddati o'tgan kod.",
        "en": "❌ Invalid or expired link code.",
    },
    "link_success": {
        "ru": "✅ Успешно привязан к **{name}**!\n\nДобро пожаловать в панель сотрудника.",
        "uz": "✅ **{name}** ga muvaffaqiyatli ulandi!\n\nXodim paneliga xush kelibsiz.",
        "en": "✅ Successfully linked to **{name}**!\n\nWelcome to your staff panel.",
    },
    "no_shops_owner": {
        "ru": "У вас пока нет заведений.", "uz": "Sizda hali muassasalar yo'q.", "en": "You don't have any shops yet.",
    },
    "your_shops_title": {
        "ru": "🏢 **Ваши заведения:**\n\n", "uz": "🏢 **Sizning muassasalaringiz:**\n\n", "en": "🏢 **Your Shops:**\n\n",
    },
    "no_staff_owner": {
        "ru": "У вас пока нет сотрудников.", "uz": "Sizda hali xodimlar yo'q.", "en": "You don't have any staff yet.",
    },
    "your_staff_title": {
        "ru": "👥 **Ваши сотрудники**\n\nНажмите на сотрудника, чтобы сгенерировать код привязки Telegram.",
        "uz": "👥 **Sizning xodimlaringiz**\n\nTelegram ulash kodini yaratish uchun xodim ustiga bosing.",
        "en": "👥 **Your Staff**\n\nTap a staff member to generate a Telegram completely link code for them.",
    },
    "status_linked": {
        "ru": "✅ Привязан", "uz": "✅ Ulangan", "en": "✅ Linked",
    },
    "status_unlinked": {
        "ru": "🔗 Сгенерировать", "uz": "🔗 Yaratish", "en": "🔗 Generate Link",
    },
    "staff_link_code": {
        "ru": "🔗 **Код привязки для {name}**\n\nОтправьте этот код сотруднику:\n\n`{code}`\n\nОн должен отправить боту:\n`/link {code}`",
        "uz": "🔗 **{name} uchun ulash kodi**\n\nUshbu kodni xodimga yuboring:\n\n`{code}`\n\nU botga shunday yuborishi kerak:\n`/link {code}`",
        "en": "🔗 **Staff Link Code for {name}**\n\nSend them this code so they can link their Telegram account:\n\n`{code}`\n\nThey should open this bot and send:\n`/link {code}`",
    },
    "no_staff_profile": {
        "ru": "Вы не привязаны к профилю сотрудника.",
        "uz": "Siz xodim profiliga ulanmagansiz.",
        "en": "You are not linked to a staff profile.",
    },
    "no_bookings_day": {
        "ru": "📅 **{title} ({date})**\n\nУ вас нет записей на этот день.",
        "uz": "📅 **{title} ({date})**\n\nBu kun uchun yozuvlaringiz yo'q.",
        "en": "📅 **{title} ({date})**\n\nYou have no bookings for this day.",
    },
    "schedule_title": {
        "ru": "📅 **{title} ({date})**\n\n",
        "uz": "📅 **{title} ({date})**\n\n",
        "en": "📅 **{title} ({date})**\n\n",
    },
    "title_today": {
        "ru": "Расписание на сегодня", "uz": "Bugungi jadval", "en": "Today's Schedule",
    },
    "title_tomorrow": {
        "ru": "Расписание на завтра", "uz": "Ertangi jadval", "en": "Tomorrow's Schedule",
    },
    "new_booking_notify": {
        "ru": "🔔 **Новая запись!**\n\n📅 {date}\n🕐 {time}\n👤 Клиент: {client}\n📞 Телефон: {phone}\n💈 Услуга: {service}",
        "uz": "🔔 **Yangi yozuv!**\n\n📅 {date}\n🕐 {time}\n👤 Mijoz: {client}\n📞 Telefon: {phone}\n💈 Xizmat: {service}",
        "en": "🔔 **New booking!**\n\n📅 {date}\n🕐 {time}\n👤 Client: {client}\n📞 Phone: {phone}\n💈 Service: {service}",
    },
    "owner_bookings_today": {
        "ru": "📋 **Записи на сегодня ({date}):**\n\n",
        "uz": "📋 **Bugungi yozuvlar ({date}):**\n\n",
        "en": "📋 **Today's Bookings ({date}):**\n\n",
    },
    "owner_bookings_upcoming": {
        "ru": "📋 **Ближайшие записи:**\n\n",
        "uz": "📋 **Kelgusi yozuvlar:**\n\n",
        "en": "📋 **Upcoming Bookings:**\n\n",
    },
    "no_bookings_owner": {
        "ru": "📋 Записей пока нет.",
        "uz": "📋 Hozircha yozuvlar yo'q.",
        "en": "📋 No bookings yet.",
    },
    "btn_today_bookings": {
        "ru": "📅 Записи на сегодня", "uz": "📅 Bugungi yozuvlar", "en": "📅 Today's Bookings",
    },
    "btn_upcoming_bookings": {
        "ru": "🔜 Ближайшие записи", "uz": "🔜 Kelgusi yozuvlar", "en": "🔜 Upcoming Bookings",
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
