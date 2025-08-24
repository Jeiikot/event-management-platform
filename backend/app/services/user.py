# Third-party imports
from sqlalchemy.exc import IntegrityError

# Local imports
from app.core.exceptions import FlowException
from app.core.security import hash_password, create_access_token
from app.crud.user import create_user_db, get_by_email


def create_user_service(db, email: str, password: str) -> str:
    if get_by_email(db, email):
        raise FlowException("Email already registered")
    try:
        user = create_user_db(db, email, hash_password(password))
        db.commit()
    except IntegrityError:
        db.rollback()
        raise FlowException("Email already registered")

    return create_access_token(user.email)
