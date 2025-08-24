# Third-party imports
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Local imports
from app.models.base import Base


class SpeakerModel(Base):
    __tablename__ = "speaker"
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255))
    bio: Mapped[str | None]

    sessions: Mapped[list["SessionModel"]] = relationship(
        secondary="session_speaker_link",
        back_populates="speakers",
    )
