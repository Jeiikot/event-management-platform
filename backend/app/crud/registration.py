# Standard library imports
from typing import Sequence

# Third-party imports
from sqlalchemy import select
from sqlalchemy.orm import Session

# Local imports
from app.models.event import EventModel
from app.models.enums import EventStatus
from app.models.registration import EventRegistrationModel


def get_event_for_update(db: Session, event_id: int) -> EventModel | None:
    query = (
        select(EventModel)
        .where(EventModel.id == event_id, EventModel.status != EventStatus.DELETED)
        .with_for_update()
    )
    return db.execute(query).scalar_one_or_none()


def get_registration(db: Session, event_id: int, user_id: int) -> EventRegistrationModel | None:
    query = select(EventRegistrationModel).where(
        EventRegistrationModel.event_id == event_id,
        EventRegistrationModel.user_id == user_id,
    )
    return db.execute(query).scalar_one_or_none()


def create_registration(db: Session, event_id: int, user_id: int) -> EventRegistrationModel:
    registration = EventRegistrationModel(event_id=event_id, user_id=user_id)
    db.add(registration)
    db.commit()
    db.refresh(registration)
    return registration


def list_registrations_by_user(db: Session, user_id: int) -> Sequence[EventRegistrationModel]:
    query = select(EventRegistrationModel).where(EventRegistrationModel.user_id == user_id)
    return db.execute(query).scalars().all()
