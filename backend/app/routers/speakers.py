# Third-party imports
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

# Local imports
from app.dependencies.auth import get_db, get_current_user
from app.models.user import UserModel
from app.schemas.speaker import SpeakerCreate, SpeakerUpdate, SpeakerResponse
from app.services.speaker import (
    create_speaker_service,
    list_speakers_service,
    update_speaker_service,
    delete_speaker_service,
)


router = APIRouter(prefix="/speakers", tags=["Speakers"])


@router.post(
    "",
    response_model=SpeakerResponse,
    status_code=status.HTTP_201_CREATED,
    response_description="Speaker created",
)
def create_speaker(
    data: SpeakerCreate,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
) -> SpeakerResponse:
    return create_speaker_service(db, data, user.id)


@router.get(
    "",
    response_model=list[SpeakerResponse],
    response_description="List of speakers",
)
def list_speakers(
    db: Session = Depends(get_db),
) -> list[SpeakerResponse]:
    return list_speakers_service(db)


@router.patch(
    "/{speaker_id}",
    response_model=SpeakerResponse,
    response_description="Speaker updated",
)
def update_speaker(
    speaker_id: int,
    data: SpeakerUpdate,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
) -> SpeakerResponse:
    return update_speaker_service(db, speaker_id, data, user.id)


@router.delete("/{speaker_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_speaker(
    speaker_id: int,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
) -> None:
    delete_speaker_service(db, user.id, speaker_id)
