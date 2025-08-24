from typing import Generic, TypeVar, Sequence
from pydantic import BaseModel, Field

T = TypeVar("T")

class Page(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int = Field(1, ge=1)
    size: int = Field(10, ge=1, le=100)
