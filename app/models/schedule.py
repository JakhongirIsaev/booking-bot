"""
Schedule model — defines working hours for a staff member.

Each record represents one day's schedule for a staff member.
day_of_week: 0 = Monday, 6 = Sunday (ISO standard).
"""

import uuid
from datetime import time

from sqlalchemy import ForeignKey, Integer, SmallInteger, Time
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Schedule(Base):
    __tablename__ = "schedules"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    staff_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("staff.id"), nullable=False
    )
    # 0 = Monday, 1 = Tuesday, ..., 6 = Sunday
    day_of_week: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)

    # Relationships
    staff = relationship("Staff", back_populates="schedules")

    def __repr__(self) -> str:
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        day_name = days[self.day_of_week] if 0 <= self.day_of_week <= 6 else "?"
        return f"<Schedule({day_name} {self.start_time}-{self.end_time})>"
