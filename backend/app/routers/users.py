# Third-party imports
from fastapi import APIRouter, Depends, status

# Local imports
from app.dependencies.auth import get_current_user
from app.schemas.user import UserResponse


router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/me",
    response_model=UserResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid credentials",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid credentials"}
                }
            },
        },
    },
)
def me(user: UserResponse = Depends(get_current_user)) -> UserResponse:
    return user
