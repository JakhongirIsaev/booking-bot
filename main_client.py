"""
Main entry point — starts the Telegram booking bot.

Lifecycle:
1. Initialize database (create tables)
2. Seed demo data (if empty)
3. Register all Telegram handlers (routers)
4. Start aiogram long-polling

To run:
    python main.py
"""

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from app.config.settings import settings
from app.database.session import init_db, close_db, get_session
from app.database.seed import seed_database

# Import handler routers
from app.bot.handlers.start import router as start_router
from app.bot.handlers.booking import router as booking_router
from app.bot.handlers.my_bookings import router as my_bookings_router
from app.bot.handlers.admin import router as admin_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


async def on_startup(bot: Bot) -> None:
    """Run on bot startup — initialize database and seed data."""
    logger.info("🚀 Starting bot...")

    # Create database tables
    await init_db()
    logger.info("✅ Database tables created")

    # Seed demo data
    async with get_session() as session:
        await seed_database(session)

    # Log bot info
    bot_info = await bot.get_me()
    logger.info(f"🤖 Bot: @{bot_info.username} ({bot_info.full_name})")
    logger.info(f"🏪 Business: {settings.business_name}")
    logger.info(f"👤 Admin TG ID: {settings.admin_telegram_id}")
    logger.info("✅ Bot is ready!")


async def on_shutdown(bot: Bot) -> None:
    """Run on bot shutdown — cleanup resources."""
    logger.info("🛑 Shutting down...")
    await close_db()
    logger.info("✅ Database connection closed")


async def main() -> None:
    """Main function — configure and start the bot."""
    # Create bot instance
    bot = Bot(token=settings.client_bot_token)

    # Create dispatcher with in-memory FSM storage
    # (In production, consider using Redis storage for persistence)
    dp = Dispatcher(storage=MemoryStorage())

    # Register startup/shutdown hooks
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # Register handler routers (order matters — first match wins)
    dp.include_router(start_router)
    dp.include_router(booking_router)
    dp.include_router(my_bookings_router)
    dp.include_router(admin_router)

    logger.info("🔄 Starting long-polling...")

    # Start polling — the bot will listen for updates from Telegram
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
