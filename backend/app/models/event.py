# Standard library imports
from datetime import datetime
from typing import Optional

# Third-party imports
from sqlalchemy import String, Enum, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Local imports
from app.models.base import Base
from app.models.enums import EventStatus


class EventModel(Base):
    __tablename__ = "event"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str | None]
    status: Mapped[EventStatus] = mapped_column(Enum(EventStatus), default=EventStatus.DRAFT)
    venue: Mapped[str | None]
    start_at: Mapped[datetime]
    end_at: Mapped[datetime]
    capacity_total: Mapped[int] = mapped_column(Integer, default=0)
    capacity_available: Mapped[int] = mapped_column(Integer, default=0)

    sessions: Mapped[list["SessionModel"]] = relationship(back_populates="event", cascade="all, delete-orphan")
    registrations: Mapped[list["EventRegistrationModel"]] = relationship(back_populates="event", cascade="all, delete-orphan")

    created_by: Mapped[int | None] = mapped_column(ForeignKey("user.id", ondelete="SET NULL"), nullable=True)
    updated_by: Mapped[int | None] = mapped_column(ForeignKey("user.id", ondelete="SET NULL"), nullable=True)

    creator: Mapped[Optional["UserModel"]] = relationship(
        "UserModel", foreign_keys=[created_by], back_populates="created_events"
    )
    updater: Mapped[Optional["UserModel"]] = relationship(
        "UserModel", foreign_keys=[updated_by], back_populates="updated_events"
    )

