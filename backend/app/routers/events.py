# Standard library imports
from typing import Optional
# Third-party imports
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

# Local imports
from app.schemas.event import EventCreateRequest, EventUpdateRequest, EventResponse, ListEventResponse
from app.dependencies.auth import get_db, get_current_user
from app.models.user import UserModel
from app.core.pagination import Page
from app.services.event import (
    list_events_service,
    create_event_service,
    get_event_service,
    update_event_service,
    delete_event_service,
)


router = APIRouter(prefix="/events", tags=["Events"])


@router.get(
    "",
    response_model=Page[ListEventResponse],
    response_description="List of events",
)
def list_events(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    search: Optional[str] = None
) -> Page[ListEventResponse]:
    return list_events_service(db, page, size, search)


@router.post(
    "",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
    response_description="Event created",
)
def create_event(
    data: EventCreateRequest,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
) -> EventResponse:
    return create_event_service(db, data, user.id)


@router.get(
    "/{event_id}",
    response_model=EventResponse,
    response_description="Event details",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Event not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Event not found"}
                }
            },
        },
    },
)
def get_event(
    event_id: int,
    db: Session = Depends(get_db)
) -> EventResponse:
    return get_event_service(db, event_id)


@router.patch(
    "/{event_id}",
    response_model=EventResponse,
    response_description="Event updated",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Event not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Event not found"}
                }
            },
        },
    },
)
def update_event(
    event_id: int,
    data: EventUpdateRequest,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
) -> EventResponse:
    return update_event_service(db, event_id, data, user.id)


@router.delete(
    "/{event_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Event deleted",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Event not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Event not found"}
                }
            },
        },
    },
)
def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
) -> None:
    delete_event_service(db, event_id, user.id)
