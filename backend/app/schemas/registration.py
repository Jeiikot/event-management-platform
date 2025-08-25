# Third-party imports
from pydantic import BaseModel, ConfigDict


class RegistrationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    event_id: int
    user_id: int
