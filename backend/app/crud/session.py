# Standard library
from typing import Sequence

# Third-party
from sqlalchemy import select, delete
from sqlalchemy.orm import Session

# Local imports
from app.models.session import SessionModel, SessionSpeakerLinkModel
from app.models.speaker import SpeakerModel


def get_session(db: Session, session_id: int) -> SessionModel | None:
    return db.get(SessionModel, session_id)


def list_sessions_by_event(db: Session, event_id: int) -> Sequence[SessionModel]:
    sessions_query = select(SessionModel).where(SessionModel.event_id == event_id)
    return db.execute(sessions_query).scalars().all()


def create_session(db: Session, event_id: int, data: dict) -> SessionModel:
    session = SessionModel(event_id=event_id, **data)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def update_session(db: Session, session: SessionModel, fields: dict) -> SessionModel:
    for key, value in fields.items():
        setattr(session, key, value)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

def delete_session(db: Session, s: SessionModel) -> None:
    db.delete(s)
    db.commit()

def list_speakers_for_session(db: Session, session_id: int) -> Sequence[SpeakerModel]:
    query = (
        select(SpeakerModel)
        .join(SessionSpeakerLinkModel, SessionSpeakerLinkModel.speaker_id == SpeakerModel.id)
        .where(SessionSpeakerLinkModel.session_id == session_id)
    )
    return db.execute(query).scalars().all()

def set_session_speakers(db: Session, session_id: int, speaker_ids: list[int]) -> None:
    db.execute(delete(SessionSpeakerLinkModel).where(SessionSpeakerLinkModel.session_id == session_id))

    if not speaker_ids:
        return

    for sp_id in speaker_ids:
        db.add(SessionSpeakerLinkModel(session_id=session_id, speaker_id=sp_id))
    db.commit()

def filter_existing_speaker_ids(db: Session, speaker_ids: list[int]) -> list[int]:
    if not speaker_ids:
        return []
    rows = db.execute(select(SpeakerModel.id).where(SpeakerModel.id.in_(speaker_ids))).scalars().all()
    return list(rows)
