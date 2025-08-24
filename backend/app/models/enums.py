# Standard library imports
from enum import Enum


class EventStatus(str, Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    CANCELLED = "CANCELLED"
    FINISHED = "FINISHED"
    DELETED = "DELETED"
