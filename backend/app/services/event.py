# Standard library imports
from typing import Optional

# Third-party imports
from sqlalchemy.orm import Session

# Local imports
from app.core.exceptions import ResourceNotFoundException
from app.crud.event import list_events, create_event, get_event, list_sessions_by_event, update_event, soft_delete_event
from app.schemas.event import  EventUpdateRequest, EventResponse, ListEventResponse, EventCreateRequest
from app.core.pagination import Page
from app.schemas.session import SessionBasicResponse


def _build_event_response(db: Session, event: EventResponse) -> EventResponse:
    sessions = list_sessions_by_event(db, event.id)
    response = EventResponse.model_validate(event)
    response.sessions = [SessionBasicResponse.model_validate(session) for session in sessions]
    return response

def list_events_service(db: Session, page: int, size: int, search: Optional[str]) -> Page[ListEventResponse]:
    events, total = list_events(db, page, size, search)
    items = [
        ListEventResponse(
            id=event.id, name=event.name, status=event.status, start_at=event.start_at, end_at=event.end_at,
            capacity_available=event.capacity_available
        )
        for event in events
    ]
    return Page(items=items, total=total, page=page, size=size)


def create_event_service(db: Session, data: EventCreateRequest, user_id: int) -> EventResponse:
    event = create_event(db, data=data.model_dump(), user_id=user_id)
    return EventResponse.model_validate(event)


def get_event_service(db: Session, event_id: int) -> EventResponse:
    event = get_event(db, event_id)
    if not event:
        raise ResourceNotFoundException("Event not found")
    return _build_event_response(db, event)


def update_event_service(db: Session, event_id: int, data: EventUpdateRequest, user_id: int) -> EventResponse:
    event = get_event(db, event_id)
    if not event:
        raise ResourceNotFoundException("Event not found")

    fields = data.model_dump(exclude_unset=True)
    event = update_event(db, event, fields, user_id)
    return _build_event_response(db, event)


def delete_event_service(db: Session, event_id: int, user_id: int) -> None:
    event = get_event(db, event_id)
    if not event:
        raise ResourceNotFoundException("Event not found")

    soft_delete_event(db, event, user_id)
