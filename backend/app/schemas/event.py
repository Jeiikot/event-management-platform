from pydantic import BaseModel, Field, model_validator, ConfigDict
from datetime import datetime
from typing import Optional, List

from app.models.enums import EventStatus
from app.schemas.session import SessionBasicResponse


class EventBase(BaseModel):
    @model_validator(mode="after")
    def check_capacity(self):
        if self.capacity_available > self.capacity_total:
            raise ValueError("capacity_available cannot exceed capacity_total")
        return self


class EventCreateRequest(EventBase):
    name: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    status: EventStatus = EventStatus.DRAFT
    venue: Optional[str] = None
    start_at: datetime
    end_at: datetime
    capacity_total: int = Field(ge=1)
    capacity_available: int = Field(ge=0)

class EventUpdateRequest(EventBase):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[EventStatus] = None
    venue: Optional[str] = None
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    capacity_total: Optional[int] = None
    capacity_available: Optional[int] = None

class EventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str]
    status: EventStatus
    venue: Optional[str]
    start_at: datetime
    end_at: datetime
    capacity_total: int
    capacity_available: int
    created_by: int | None
    sessions: List[SessionBasicResponse] = []

class ListEventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    status: EventStatus
    start_at: datetime
    end_at: datetime
    capacity_available: int
