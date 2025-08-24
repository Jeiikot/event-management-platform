# Local imports
from app.crud.user import get_by_email
from app.core.security import verify_password, create_access_token
from app.core.exceptions import AuthException


def login_user_service(db, email: str, password: str) -> str:
    user = get_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        raise AuthException()

    return create_access_token(user.email)
