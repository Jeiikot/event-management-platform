# Third-party imports
from sqlalchemy.orm import Session

# Local imports
from app.crud.speaker import create_speaker, list_speakers, get_speaker, update_speaker, delete_speaker
from app.schemas.speaker import SpeakerCreate, SpeakerUpdate, SpeakerResponse
from app.core.exceptions import ResourceNotFoundException


def create_speaker_service(db: Session, data: SpeakerCreate, user_id: int) -> SpeakerResponse:
    speaker = create_speaker(db, data.model_dump())
    return SpeakerResponse.model_validate(speaker)


def list_speakers_service(db: Session) -> list[SpeakerResponse]:
    speakers = list_speakers(db)
    return [SpeakerResponse.model_validate(speaker) for speaker in speakers]


def update_speaker_service(db: Session, speaker_id: int, data: SpeakerUpdate, user_id: int) -> SpeakerResponse:
    speaker = get_speaker(db, speaker_id)
    if not speaker:
        raise ResourceNotFoundException("Speaker not found")
    speaker = update_speaker(db, speaker, data.model_dump(exclude_unset=True))
    return SpeakerResponse.model_validate(speaker)


def delete_speaker_service(db: Session, speaker_id: int, user_id: int) -> None:
    speaker = get_speaker(db, speaker_id)
    if not speaker:
        raise ResourceNotFoundException("Speaker not found")
    delete_speaker(db, speaker)
