# Third-party
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

# Local
from app.dependencies.auth import get_db, get_current_user
from app.models.user import UserModel
from app.schemas.session import SessionCreate, SessionUpdate, SessionResponse
from app.services.session import (
    create_session_service,
    list_sessions_service,
    update_session_service,
    delete_session_service,
)


router = APIRouter(prefix="/sessions", tags=["Sessions"])


@router.get(
    "/events/{event_id}",
    response_model=list[SessionResponse],
    response_description="List of sessions",
)
def list_sessions(
    event_id: int,
    db: Session = Depends(get_db),
) -> list[SessionResponse]:
    return list_sessions_service(db, event_id)


@router.post(
    "/events/{event_id}",
    response_model=SessionResponse,
    status_code=status.HTTP_201_CREATED
)
def create_session(
    event_id: int,
    data: SessionCreate,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
) -> SessionResponse:
    return create_session_service(db, event_id, data, user.id)

@router.patch(
    "/{session_id}",
    response_model=SessionResponse,
    response_description="Session updated",
)
def update_session(
    session_id: int,
    data: SessionUpdate,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
) -> SessionResponse:
    return update_session_service(db, session_id, data, user.id)

@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(
    session_id: int,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
) -> None:
    delete_session_service(db, session_id, user.id)
