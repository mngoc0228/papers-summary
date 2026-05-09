from fastapi import Depends, status

from src.core.base_response import http_ok
from src.routes.user import router
from src.core.exception_model import ExceptionModel
from src.services.dependencies import get_current_user


@router.get(
    '/me',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            'model': ExceptionModel
        }
    },
)
async def me(
    current_user = Depends(get_current_user)
):
    return http_ok(data=current_user)