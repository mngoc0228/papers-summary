from typing import Any, Dict, Optional, Union
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


class BaseException(HTTPException):
    def __init__(
            self,
            status_code: int = 500,
            message: str = "Server Internal Error",
            detail: Optional[Union[Dict[str, Any], list, str]] = None,
            **kwargs
    ) -> None:
        content = {
            'status': status_code,
            'message': message,
            'detail': detail
        }

        try:
            content = {k: v for k, v in content.items() if v is not None}
            content = jsonable_encoder(content)
        except Exception as e:
            content = {
                'status': status_code,
                'message': message,
                'detail': str(e)
            }

        super().__init__(status_code=status_code, detail=content, **kwargs)

    def to_response(self) -> JSONResponse:
        """Convert the exception to a JSONResponse."""
        return JSONResponse(
            status_code=self.status_code,
            content=self.detail
        )


class NotFoundError(BaseException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, message=message)


class UnauthorizedError(BaseException):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, message=message)


class BadRequestError(BaseException):
    def __init__(self, message: str = "Bad request", detail: Optional[Any] = None):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, message=message, detail=detail)


class ValidationError(BaseException):
    def __init__(self, message: str = "Validation error", detail: Optional[Any] = None):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, message=message, detail=detail)


class ForbiddenError(BaseException):
    def __init__(self, message: str = "Forbidden", detail: Optional[Any] = None):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, message=message, detail=detail)


class ConflictError(BaseException):
    def __init__(self, message: str = "Conflict", detail: Optional[Any] = None):
        super().__init__(status_code=status.HTTP_409_CONFLICT, message=message, detail=detail)


class InternalServerError(BaseException):
    def __init__(self, message: str = "Internal Server Error", detail: Optional[Any] = None):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=message, detail=detail)
