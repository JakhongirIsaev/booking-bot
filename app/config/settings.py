"""
Application settings loaded from environment variables.

Uses pydantic-settings to validate and parse configuration.
All values are loaded from .env file or environment variables.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration."""

    # Telegram bot token from @BotFather
    bot_token: str

    # PostgreSQL async connection string
    database_url: str = "postgresql+asyncpg://booking_user:booking_pass@localhost:5432/booking_db"

    # Telegram user ID of the admin / business owner
    admin_telegram_id: int = 0

    # Business name displayed in bot messages
    business_name: str = "Demo Barbershop"

    # Timezone for the business
    timezone: str = "Asia/Tashkent"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Singleton settings instance — import this everywhere
settings = Settings()
