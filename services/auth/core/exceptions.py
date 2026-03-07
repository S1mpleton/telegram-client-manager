from fastapi import HTTPException, status

class BaseAppException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: str,
        headers: dict = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)

class NotFoundException(BaseAppException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )

class UnauthorizedException(BaseAppException):
    def __init__(self, detail: str = "Invalid credentials"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )

class ForbiddenException(BaseAppException):
    def __init__(self, detail: str = "Access forbidden"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )

class ConflictException(BaseAppException):
    def __init__(self, detail: str = "Data conflict"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail
        )

class ValidationException(BaseAppException):
    def __init__(self, detail: str = "Validation error"):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        )

class InternalServerException(BaseAppException):
    def __init__(self, detail: str = "Internal server error"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )