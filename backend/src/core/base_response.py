from typing import Any, Dict, Optional, Union

from fastapi import Query, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi_pagination import Params


class BaseJsonResponse(JSONResponse):
    def __init__(
            self,
            status_code: int = 200,
            success: bool = True,
            message: str = "Success",
            data: Optional[Union[Dict[str, Any], list]] = None,
            errors: Optional[Union[Dict[str, Any], list, str]] = None,
            page: Optional[int] = None,
            size: Optional[int] = None,
            total: Optional[int] = None,
            pages: Optional[int] = None,
            **kwargs,
    ) -> None:
        content = {
            'status': status_code,
            'success': success,
            'message': message,
            'data': data,
            'errors': errors
        }

        # Add pagination metadata if provided
        if page is not None and size is not None and total is not None and pages is not None:
            pagination_info = {
                'page': page,
                'size': size,
                'total': total,
                'pages': pages
            }
            content.update(pagination_info)
            content['data'] = data

        content = {k: v for k, v in content.items() if v is not None or k in ['data']}

        super().__init__(status_code=status_code, content=jsonable_encoder(content), **kwargs)


def http_response(status_code: int, data: Optional[Any] = None, success: bool = True, message: str = '',
                  errors: Optional[Any] = None):
    return BaseJsonResponse(status_code=status_code, success=success, message=message, data=data, errors=errors)


def http_ok(
        data: Optional[Any] = None,
        success: bool = True,
        message: str = 'Success',
        page: Optional[int] = None,
        size: Optional[int] = None,
        total: Optional[int] = None,
        pages: Optional[int] = None
):
    return BaseJsonResponse(
        status_code=status.HTTP_200_OK,
        success=success,
        message=message,
        data=data,
        page=page,
        size=size,
        total=total,
        pages=pages
    )


def http_created(data: Optional[Any] = None, message: str = 'Created successfully'):
    return http_response(status_code=status.HTTP_201_CREATED, data=data, message=message)


def http_not_found(message: str = 'Not Found'):
    return http_response(status_code=status.HTTP_404_NOT_FOUND, success=False, message=message)


def http_bad_request(error_message: Union[str, list] = "Bad Request"):
    return http_response(status_code=status.HTTP_400_BAD_REQUEST, success=False, errors=error_message)

class CustomParams(Params):
    page: int = Query(1, ge=1, description="Page number")
    size: int = Query(50, ge=1, le=5000, description="Page size")