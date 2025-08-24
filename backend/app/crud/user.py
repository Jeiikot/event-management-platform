# Third-party imports
from sqlalchemy import select

# Local imports
from app.models.user import UserModel


def get_by_email(db, email: str) -> UserModel | None:
    query = select(UserModel).where(UserModel.email == email)
    return db.execute(query).scalar_one_or_none()


def create_user_db(db, email: str, hashed_password: str) -> UserModel:
    user = UserModel(email=email, hashed_password=hashed_password)
    db.add(user)
    db.flush()
    db.refresh(user)
    return user
