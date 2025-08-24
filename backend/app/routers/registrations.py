# Third-party imports
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

# Local imports
from app.dependencies.auth import get_db, get_current_user
from app.models.user import UserModel
from app.schemas.registration import RegistrationResponse
from app.services.registration import register_event_service, my_registrations_service


router = APIRouter(prefix="/registrations", tags=["Registrations"])


@router.post(
    "/events/{event_id}",
    response_model=RegistrationResponse,
    status_code=status.HTTP_201_CREATED,
    response_description="Registration created",
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "Conflict: event is full or user already registered",
            "content": {
                "application/json": {
                    "examples": {
                        "event_full": {
                            "summary": "Event full",
                            "value": {"detail": "Event full"}
                        },
                        "already_registered": {
                            "summary": "Already registered",
                            "value": {"detail": "Already registered"}
                        },
                    }
                }
            },
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Event not found",
            "content": {"application/json": {"example": {"detail": "Event not found"}}},
        },
    },
)
def create_registration(
    event_id: int,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
) -> RegistrationResponse:
    return register_event_service(db, event_id, user.id)


@router.get(
    "/events",
    response_model=list[RegistrationResponse],
    response_description="List of my registrations",
)
def my_registrations(
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
) -> list[RegistrationResponse]:
    return my_registrations_service(db, user.id)
