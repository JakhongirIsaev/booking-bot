"""
Application settings loaded from environment variables.

Uses pydantic-settings to validate and parse configuration.
All values are loaded from .env file or environment variables.
"""

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application configuration."""

    # Telegram bot token for the client-facing bot
    client_bot_token: str = Field(alias="CLIENT_BOT_TOKEN", default="")
    # Telegram bot token for the business-facing bot
    business_bot_token: str = Field(alias="BUSINESS_BOT_TOKEN", default="")

    # PostgreSQL async connection string
    database_url: str = Field(alias="DATABASE_URL", default="postgresql+asyncpg://postgres:postgres@localhost:5432/booking_db")

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
