from pydantic import BaseModel, Field, ConfigDict, model_validator
from datetime import datetime
from typing import Optional, List

from app.schemas.speaker import SpeakerResponse


class SessionBase(BaseModel):
    @model_validator(mode="after")
    def check_capacity(self):
        if self.capacity_available > self.capacity_total:
            raise ValueError("capacity_available cannot exceed capacity_total")
        return self


class SessionCreate(SessionBase):
    title: str = Field(min_length=1)
    description: Optional[str] = None
    start_at: datetime
    end_at: datetime
    room: Optional[str] = None
    capacity_total: int = Field(ge=1)
    capacity_available: int = Field(ge=0)
    speaker_ids: List[int] = []


class SessionUpdate(SessionBase):
    title: Optional[str] = None
    description: Optional[str] = None
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    room: Optional[str] = None
    capacity_total: Optional[int] = None
    capacity_available: Optional[int] = None
    speaker_ids: Optional[List[int]] = None


class SessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    event_id: int
    title: str
    description: Optional[str]
    start_at: datetime
    end_at: datetime
    room: Optional[str]
    capacity_total: int
    capacity_available: int
    speakers: List[SpeakerResponse] = []

class SessionBasicResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    start_at: datetime
    end_at: datetime
