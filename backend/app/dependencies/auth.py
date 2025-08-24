# Third-party imports
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

# Local imports
from app.core.db import get_session
from app.core.exceptions import AuthException
from app.core.security import decode_token
from app.crud.user import get_by_email
from app.models.user import UserModel


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_db(session: Session = Depends(get_session)):
    return session


def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
) -> UserModel:
    payload = decode_token(token)
    if not payload or "sub" not in payload:
        raise AuthException("Invalid token")

    email = payload["sub"]
    user = get_by_email(db, email)

    if not user or not user.is_active:
        raise AuthException("Invalid token")
    return user
