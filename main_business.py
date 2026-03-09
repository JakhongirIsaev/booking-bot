"""
Entrypoint for the Business & Staff Bot.

This bot is for internal use:
- Owners can view their shops and all bookings.
- Staff (barbers/masters) can view their personal schedule.
"""

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from app.config.settings import settings
from app.database.session import close_db

# We'll create these routers next
from app.bot_business.handlers.start import router as start_router
from app.bot_business.handlers.owner import router as owner_router
from app.bot_business.handlers.staff import router as staff_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


async def on_startup(bot: Bot) -> None:
    logger.info("🚀 Starting Business & Staff bot...")
    bot_info = await bot.get_me()
    logger.info(f"🤖 Bot: @{bot_info.username} ({bot_info.full_name})")
    logger.info("✅ Business Bot is ready!")


async def on_shutdown(bot: Bot) -> None:
    logger.info("🛑 Shutting down Business Bot...")
    await close_db()


async def main() -> None:
    if not settings.business_bot_token:
        logger.error("❌ BUSINESS_BOT_TOKEN is not set. Business bot cannot start.")
        return

    bot = Bot(token=settings.business_bot_token)
    dp = Dispatcher(storage=MemoryStorage())

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # Register routers (created in next steps)
    dp.include_router(start_router)
    dp.include_router(owner_router)
    dp.include_router(staff_router)

    logger.info("🔄 Starting long-polling for Business Bot...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
