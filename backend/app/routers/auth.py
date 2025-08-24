# Third-party imports
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

# Local imports
from app.dependencies.auth import get_db
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.services.auth import login_user_service
from app.services.user import create_user_service


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    response_description="User created",
    summary="Register a new user",
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "Email already registered",
            "content": {
                "application/json": {
                    "example": {"detail": "Email already registered"}
                }
            },
        },
    }
)
def create_user(data: RegisterRequest, db: Session = Depends(get_db)) -> TokenResponse:
    token = create_user_service(db, data.email, data.password)
    return TokenResponse(access_token=token)


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    response_description="User logged in",
    summary="Login a user",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid credentials",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid credentials"}
                }
            },
        },
    }

)
def login(data: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    token = login_user_service(db, data.email, data.password)
    return TokenResponse(access_token=token)
