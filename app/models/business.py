"""
Business model — represents a service business (barbershop, nail salon, etc.).

Each business has a category, location, and optional owner.
Contains staff, services, and bookings.
"""

import uuid
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Business(Base):
    __tablename__ = "businesses"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False, default="barbershop")
    address: Mapped[str | None] = mapped_column(String(500), nullable=True)
    telegram_owner_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    staff = relationship("Staff", back_populates="business", lazy="selectin")
    services = relationship("Service", back_populates="business", lazy="selectin")
    bookings = relationship("Booking", back_populates="business", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Business(id={self.id}, name='{self.name}', cat='{self.category}')>"
