# Standard library imports
from typing import Optional

# Third-party imports
from pydantic import BaseModel, ConfigDict


class SpeakerBase(BaseModel):
    full_name: str
    bio: Optional[str] = None


class SpeakerCreate(SpeakerBase):
    pass


class SpeakerUpdate(BaseModel):
    full_name: Optional[str] = None
    bio: Optional[str] = None


class SpeakerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    bio: Optional[str]
