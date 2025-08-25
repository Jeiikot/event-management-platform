
# Standard library imports
from datetime import datetime, timedelta


def make_event_payload(**overrides) -> dict:
    """Factory for a minimal valid event payload."""
    default_payload = {
        "name": "TechConf",
        "description": "Annual conf",
        "venue": "Neiva Arena",
        "start_at": (datetime.utcnow() + timedelta(days=1)).isoformat(),
        "end_at": (datetime.utcnow() + timedelta(days=1, hours=3)).isoformat(),
        "capacity_total": 100,
        "capacity_available": 100,
    }
    default_payload.update(overrides)
    return default_payload


def make_session_payload(**overrides) -> dict:
    """Factory for a minimal valid session payload."""
    default_payload = {
        "title": "Opening Keynote",
        "description": "Welcome session",
        "room": "A1",
        "start_at": (datetime.utcnow() + timedelta(days=1, hours=1)).isoformat(),
        "end_at": (datetime.utcnow() + timedelta(days=1, hours=2)).isoformat(),
        "capacity_total": 50,
        "capacity_available": 50,
        "speaker_ids": [],
    }
    default_payload.update(overrides)
    return default_payload
