"""
Client Service — manages client (customer) records.

Clients are auto-created when they first interact with the bot.
Each client is identified by their unique Telegram user ID.
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
) -> Client:
    """
    Get an existing client or create a new one.

    Called every time a user sends /start or begins a booking.
    If the client exists, returns the existing record.
    If not, creates a new client with the given name.

    Args:
        telegram_id: User's Telegram ID
        name: User's display name from Telegram

    Returns:
        Client object (existing or newly created)
    """
    result = await session.execute(
        select(Client).where(Client.telegram_id == telegram_id)
    )
    client = result.scalar_one_or_none()

    if client is not None:
        # Update name if changed
        if client.name != name:
            client.name = name
            await session.flush()
        return client

    # Create new client
    client = Client(
        telegram_id=telegram_id,
        name=name,
    )
    session.add(client)
    await session.flush()
    return client


async def get_client_by_telegram_id(
    session: AsyncSession,
    telegram_id: int,
) -> Optional[Client]:
    """Look up a client by their Telegram ID."""
    result = await session.execute(
        select(Client).where(Client.telegram_id == telegram_id)
    )
    return result.scalar_one_or_none()
