# Third-party imports
from sqlalchemy.orm import Session

# Local imports
from app.core.exceptions import ResourceNotFoundException, FlowException
from app.crud.registration import get_registration, create_registration, list_registrations_by_user, get_event_for_update
from app.schemas.registration import RegistrationResponse


def register_event_service(db: Session, event_id: int, user_id: int) -> RegistrationResponse:
    event = get_event_for_update(db, event_id)

    if not event:
        raise ResourceNotFoundException("Event not found")

    if event.capacity_available <= 0:
        raise FlowException("Event full")

    if get_registration(db, event_id, user_id):
        raise FlowException("User already registered")

    event.capacity_available -= 1
    registration = create_registration(db, event_id, user_id)

    return RegistrationResponse.model_validate(registration)


def my_registrations_service(db: Session, user_id: int) -> list[RegistrationResponse]:
    registrations = list_registrations_by_user(db, user_id)
    return [RegistrationResponse.model_validate(registration) for registration in registrations]
