# Third-party imports
from fastapi import HTTPException, status


class APIException(HTTPException):
    pass


class AuthException(HTTPException):
    def __init__(self, detail="Invalid credentials"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class ResourceNotFoundException(APIException):
    def __init__(self, detail: str | dict[str, str]) -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class FlowException(APIException):
    def __init__(self, detail: str | dict[str, str]) -> None:
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class PlatformPermissionException(APIException):
    def __init__(self, detail: str | dict[str, str]) -> None:
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class AppInternalException(APIException):
    def __init__(self, detail: str | dict[str, str]) -> None:
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

