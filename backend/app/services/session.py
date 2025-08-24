# Local imports
from app.schemas.session import SessionCreate, SessionUpdate, SessionResponse
from app.schemas.speaker import SpeakerResponse
from app.core.exceptions import ResourceNotFoundException
from app.crud.event import get_event
from app.crud.session import *


def _build_session_response(db: Session, session: SessionModel) -> SessionResponse:
    response = SessionResponse.model_validate(session)
    speakers = list_speakers_for_session(db, session.id)
    response.speakers = [SpeakerResponse.model_validate(speaker) for speaker in speakers]
    return response


def create_session_service(
    db: Session, event_id: int, data: SessionCreate, user_id: int
) -> SessionResponse:
    if not get_event(db, event_id):
        raise ResourceNotFoundException("Event not found")

    session = create_session(db, event_id, data.model_dump(exclude={"speaker_ids"}))

    if getattr(data, "speaker_ids"):
        speaker_ids = filter_existing_speaker_ids(db, data.speaker_ids)
        set_session_speakers(db, session.id, speaker_ids)

    return _build_session_response(db, session)


def list_sessions_service(db: Session, event_id: int) -> list[SessionResponse]:
    sessions = list_sessions_by_event(db, event_id)
    return [_build_session_response(db, session) for session in sessions]


def update_session_service(
        db: Session, session_id: int, data: SessionUpdate, user_id: int
) -> SessionResponse:
    session = get_session(db, session_id)
    if not session:
        raise ResourceNotFoundException("Session not found")

    fields = data.model_dump(exclude_unset=True, exclude={"speaker_ids"})
    session = update_session(db, session, fields)

    if getattr(data, "speaker_ids"):
        speaker_ids = filter_existing_speaker_ids(db, data.speaker_ids)
        set_session_speakers(db, session.id, speaker_ids)

    return _build_session_response(db, session)


def delete_session_service(db: Session, session_id: int, user_id: int) -> None:
    session = get_session(db, session_id)
    if not session:
        raise ResourceNotFoundException("Session not found")
    delete_session(db, session)
