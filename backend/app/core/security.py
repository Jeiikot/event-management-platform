# Standard library imports
from datetime import datetime, timedelta, timezone

# Third-party imports
from jose import jwt, JWTError
from passlib.context import CryptContext

# Local imports
from app.core.config import get_settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


def _now() -> datetime:
    return datetime.now(timezone.utc)


def create_access_token(subject: str, expires_minutes: int | None = None) -> str:
    settings = get_settings()
    exp_minutes = expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    now = _now()
    to_encode = {
        "sub": subject,
        "exp": int((now + timedelta(minutes=exp_minutes)).timestamp())
    }
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, get_settings().SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
