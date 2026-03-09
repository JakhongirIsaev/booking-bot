"""
Client Service — manages client (customer) records.

Clients are registered when they first interact with the bot.
Each client is identified by their unique Telegram user ID.
Supports language preference storage.
"""

import uuid
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.client import Client


async def get_or_create_client(
    session: AsyncSession,
    telegram_id: int,
    name: str,
    language: str = "ru",
) -> Client:
    """
    Get an existing client or create a new one.

    Args:
        telegram_id: User's Telegram ID
        name: User's display name
        language: Language code ("ru", "uz", "en")

    Returns:
        Client object (existing or newly created)
    """
    result = await session.execute(
        select(Client).where(Client.telegram_id == telegram_id)
    )
    client = result.scalar_one_or_none()

    if client is not None:
        return client

    # Create new client
    client = Client(
        telegram_id=telegram_id,
        name=name,
        language=language,
    )
    session.add(client)
    await session.flush()
    return client


async def update_client_language(
    session: AsyncSession,
    telegram_id: int,
    language: str,
) -> None:
    """Update a client's language preference."""
    result = await session.execute(
        select(Client).where(Client.telegram_id == telegram_id)
    )
    client = result.scalar_one_or_none()
    if client:
        client.language = language
        await session.flush()


async def update_client_name(
    session: AsyncSession,
    telegram_id: int,
    name: str,
) -> None:
    """Update a client's name."""
    result = await session.execute(
        select(Client).where(Client.telegram_id == telegram_id)
    )
    client = result.scalar_one_or_none()
    if client:
        client.name = name
        await session.flush()


async def update_client_phone(
    session: AsyncSession,
    telegram_id: int,
    phone: str,
) -> None:
    """Update a client's phone number."""
    result = await session.execute(
        select(Client).where(Client.telegram_id == telegram_id)
    )
    client = result.scalar_one_or_none()
    if client:
        client.phone = phone
        await session.flush()


async def get_client_by_telegram_id(
    session: AsyncSession,
    telegram_id: int,
) -> Optional[Client]:
    """Look up a client by their Telegram ID."""
    result = await session.execute(
        select(Client).where(Client.telegram_id == telegram_id)
    )
    return result.scalar_one_or_none()


async def get_client_language(
    session: AsyncSession,
    telegram_id: int,
) -> str:
    """Get a client's language preference. Returns 'ru' as default."""
    client = await get_client_by_telegram_id(session, telegram_id)
    return client.language if client else "ru"
