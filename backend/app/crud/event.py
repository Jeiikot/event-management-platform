# Standard library imports
from typing import Optional, Sequence, Tuple

# Third-party imports
from sqlalchemy.orm import Session
from sqlalchemy import func, select


# Local imports
from app.models.event import EventModel
from app.models.enums import EventStatus
from app.models.session import SessionModel


def list_events(db: Session, page: int, size: int, search: Optional[str]) -> Tuple[Sequence[EventModel], int]:
    events_query = select(EventModel).where(EventModel.status != EventStatus.DELETED)
    count_query = select(func.count(EventModel.id)).where(EventModel.status != EventStatus.DELETED)

    if search:
        like_pattern = f"%{search.strip()}%"
        events_query = events_query.where(EventModel.name.ilike(like_pattern))
        count_query = count_query.where(EventModel.name.ilike(like_pattern))

    total_count = db.execute(count_query).scalar_one()
    page_items = db.execute(
        events_query.order_by(EventModel.start_at).offset((page - 1) * size).limit(size)
    ).scalars().all()

    return page_items, total_count


def get_event(db: Session, event_id: int) -> EventModel | None:
    return db.execute(
        select(EventModel).where(
            EventModel.id == event_id,
            EventModel.status != EventStatus.DELETED,
        )
    ).scalar_one_or_none()


def list_sessions_by_event(db: Session, event_id: int) -> Sequence[SessionModel]:
    query = select(SessionModel).where(
        SessionModel.event_id == event_id, EventModel.status != EventStatus.DELETED
    )
    return db.execute(query).scalars().all()


def create_event(db: Session, data: dict, user_id: int) -> EventModel:
    event = EventModel(**data, created_by=user_id, updated_by=user_id)
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def update_event(db: Session, event : EventModel, fields: dict, user_id: int) -> EventModel:
    for key, value in fields.items():
        setattr(event, key, value)
    event.updated_by = user_id
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def soft_delete_event(db: Session, event: EventModel, user_id: int) -> EventModel:
    event.status = EventStatus.DELETED
    event.updated_by = user_id

    db.add(event)
    db.commit()
    db.refresh(event)
    return event
