# Standard library imports
from typing import Sequence

# Third-party imports
from sqlalchemy.orm import Session
from sqlalchemy import select

# Local imports
from app.models.speaker import SpeakerModel


def get_speaker(db: Session, speaker_id: int) -> SpeakerModel | None:
    return db.get(SpeakerModel, speaker_id)

def list_speakers(db: Session) -> Sequence[SpeakerModel]:
    query = select(SpeakerModel).order_by(SpeakerModel.full_name)
    return db.execute(query).scalars().all()

def create_speaker(db: Session, data: dict) -> SpeakerModel:
    speaker = SpeakerModel(**data)
    db.add(speaker)
    db.commit()
    db.refresh(speaker)
    return speaker

def update_speaker(db: Session, speaker: SpeakerModel, fields: dict) -> SpeakerModel:
    for key, value in fields.items():
        setattr(speaker, key, value)
    db.add(speaker)
    db.commit()
    db.refresh(speaker)
    return speaker

def delete_speaker(db: Session, speaker: SpeakerModel) -> None:
    db.delete(speaker)
    db.commit()
