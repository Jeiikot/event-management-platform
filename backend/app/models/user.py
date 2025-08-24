# Third-party imports
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

# Local imports
from app.models.base import Base

class UserModel(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    hashed_password: Mapped[str]
    role: Mapped[str] = mapped_column(default="ATTENDEE")

    registrations: Mapped[list["EventRegistrationModel"]] = relationship(back_populates="user")

    created_events: Mapped[list["EventModel"]] = relationship(
        "EventModel", foreign_keys="EventModel.created_by", back_populates="creator"
    )
    updated_events: Mapped[list["EventModel"]] = relationship(
        "EventModel", foreign_keys="EventModel.updated_by", back_populates="updater"
    )

