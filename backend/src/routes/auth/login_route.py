from fastapi import Depends, status

from src.core.base_response import http_ok
from src.dto.auth_dto import AuthDto
from src.routes.auth import router
from src.core.exception_model import ExceptionModel
from src.services.auth.auth_service import AuthServiceImpl
from src.services.dependencies import get_auth_service
from src.core.handle_exception import UnauthorizedError


@router.post(
    '/login',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            'model': ExceptionModel,
        },
    }
)
async def login(
    data: AuthDto,
    auth_service: AuthServiceImpl = Depends(get_auth_service),
):
    try:
        result = await auth_service.authenticate(data.email, data.password)
        if not result:
            raise UnauthorizedError('Invalid email or password')
        access_token = result.get('access_token') if result else None
        
        return http_ok(data={"access_token": access_token})
    except Exception as e:
        raise 
