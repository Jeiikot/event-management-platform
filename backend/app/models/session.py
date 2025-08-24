# Standard library imports
from datetime import datetime

# Third-party imports
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Local imports
from app.models.base import Base


class SessionSpeakerLinkModel(Base):
    __tablename__ = "session_speaker_link"

    session_id: Mapped[int] = mapped_column(ForeignKey("session.id"), primary_key=True)
    speaker_id: Mapped[int] = mapped_column(ForeignKey("speaker.id"), primary_key=True)


class SessionModel(Base):
    __tablename__ = "session"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("event.id"), index=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None]
    start_at: Mapped[datetime]
    end_at: Mapped[datetime]
    room: Mapped[str | None]
    capacity_total: Mapped[int] = mapped_column(Integer, default=0)
    capacity_available: Mapped[int] = mapped_column(Integer, default=0)

    event: Mapped["EventModel"] = relationship(back_populates="sessions")
    speakers: Mapped[list["SpeakerModel"]] = relationship(
        secondary="session_speaker_link",
        back_populates="sessions",
    )
