# 💈 Telegram Booking Bot

A Telegram-native booking platform for barbershops and service businesses. Inspired by [Altegio](https://alteg.io).

## 🏗️ Architecture

```
Telegram User ──→ aiogram Bot ──→ Service Layer ──→ PostgreSQL
                                      │
                                 ┌────┼────┐
                              Booking  Schedule  Client
                              Service  Service   Service
```

**Key principle:** Business logic lives in the service layer, NOT in Telegram handlers. This enables future expansion to web/mobile interfaces.

## ✨ Features

### Client Side (Telegram)
- 📅 **Book appointment** — Choose service → barber → date → time → confirm
- 📋 **My bookings** — View upcoming appointments with cancel option
- 🔄 **Back navigation** — Navigate back through booking steps

### Admin Side (Telegram)
- 📅 **Today's bookings** — Overview of current day's schedule
- 📋 **Upcoming bookings** — All future appointments
- 📊 **Statistics** — Total bookings, today's count, unique clients

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Bot Framework | **aiogram 3.x** |
| Database | **PostgreSQL 16** |
| ORM | **SQLAlchemy 2.x** (async) |
| DB Driver | **asyncpg** |
| Config | **pydantic-settings** |
| Deployment | **Docker + Docker Compose** |

## 📁 Project Structure

```
booking-bot/
├── main.py                     # Entry point — starts the bot
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container build
├── docker-compose.yml          # PostgreSQL + bot
├── .env.example                # Environment template
│
├── app/
│   ├── config/
│   │   └── settings.py         # App configuration (from .env)
│   │
│   ├── database/
│   │   ├── base.py             # SQLAlchemy declarative base
│   │   ├── session.py          # Async session factory
│   │   └── seed.py             # Demo data seeder
│   │
│   ├── models/                 # Database models
│   │   ├── business.py         # Business entity
│   │   ├── staff.py            # Staff / barbers
│   │   ├── service.py          # Services (Haircut, etc.)
│   │   ├── client.py           # Clients (auto-registered)
│   │   ├── schedule.py         # Working hours per day
│   │   └── booking.py          # Appointments + status enum
│   │
│   ├── services/               # Business logic (NO Telegram code here)
│   │   ├── booking_service.py  # Create/cancel/list bookings
│   │   ├── schedule_service.py # ⭐ Core slot generation algorithm
│   │   └── client_service.py   # Client get-or-create
│   │
│   └── bot/
│       ├── states.py           # FSM states for booking flow
│       ├── handlers/
│       │   ├── start.py        # /start + main menu
│       │   ├── booking.py      # 5-step booking FSM
│       │   ├── my_bookings.py  # View/cancel bookings
│       │   └── admin.py        # Admin panel (restricted)
│       └── keyboards/
│           ├── client_kb.py    # Client inline keyboards
│           └── admin_kb.py     # Admin inline keyboards
```

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# 1. Clone the repo
git clone https://github.com/JakhongirIsaev/booking-bot.git
cd booking-bot

# 2. Configure environment
cp .env.example .env
# Edit .env with your BOT_TOKEN and ADMIN_TELEGRAM_ID

# 3. Start everything
docker-compose up -d

# 4. Check logs
docker-compose logs -f bot
```

### Option 2: Local Development

```bash
# 1. Prerequisites: Python 3.12+, PostgreSQL running

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env — set BOT_TOKEN, DATABASE_URL, ADMIN_TELEGRAM_ID

# 5. Run the bot
python main.py
```

## ⚙️ Configuration

| Variable | Description | Example |
|----------|------------|---------|
| `BOT_TOKEN` | Telegram bot token from [@BotFather](https://t.me/BotFather) | `123456:ABC-DEF...` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://user:pass@localhost/db` |
| `ADMIN_TELEGRAM_ID` | Admin's Telegram user ID | `123456789` |
| `BUSINESS_NAME` | Name shown in bot messages | `Demo Barbershop` |
| `TIMEZONE` | Business timezone | `Asia/Tashkent` |

> **Get your Telegram ID:** Send `/start` to [@userinfobot](https://t.me/userinfobot)

## 🧠 Core Algorithm: Slot Generation

The slot generation in `schedule_service.py` is the heart of the system:

```
Schedule: 10:00–18:00
Service:  45 minutes

Step 1: Generate candidates
  10:00, 10:45, 11:30, 12:15, 13:00, 13:45, ...

Step 2: Remove occupied (existing bookings)
  10:00 ❌ (booked), 10:45 ✅, 11:30 ✅, ...

Step 3: Remove past (if today)
  Past slots filtered out

Result: Available time slots for the user
```

## 📊 Database Schema

```
businesses ──┬── staff ──── schedules
             ├── services
             └── bookings ──┬── clients
                            ├── staff
                            └── services
```

6 core tables: `businesses`, `staff`, `services`, `clients`, `schedules`, `bookings`

## 📱 User Flow

```
/start
  ├── 📅 Book Appointment
  │     ├── Choose Service (Haircut / Beard / Combo)
  │     ├── Choose Barber (Ali / Bek / Sardor)
  │     ├── Choose Date (next 7 days)
  │     ├── Choose Time (available slots)
  │     └── ✅ Confirm
  │
  └── 📋 My Bookings
        └── ❌ Cancel booking

/admin (restricted)
  ├── 📅 Today's Bookings
  ├── 📋 Upcoming Bookings
  └── 📊 Statistics
```

## 🗺️ Roadmap

### Phase 1 ✅ — MVP (Current)
- Client booking flow
- Admin booking viewer
- Demo data seeding

### Phase 2 — Enhanced
- ⏰ Reminders (24h, 2h, 15min before)
- 💳 Payments (Click, Payme, QR)
- 🔄 Rescheduling
- 📊 Analytics dashboard

### Phase 3 — Scale
- 🏢 Multi-location businesses
- ⭐ Reviews and ratings
- 🎁 Loyalty programs
- 🌐 Web booking page

## 📜 License

MIT
