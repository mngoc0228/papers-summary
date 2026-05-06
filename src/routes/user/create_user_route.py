from fastapi import Depends, status

from src.core.handle_exception import ConflictError, InternalServerError, NotFoundError
from src.dto.user_dto import UserCreateDto
from src.routes.user import router
from src.core.exception_model import ExceptionModel
from src.services.dependencies import get_user_service
from src.services.user.user_service import UserServiceImpl
from src.utils.security import hash_password


@router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {
            'model': ExceptionModel
        }
    },
)
async def create_user(
    data: UserCreateDto,
    user_service: UserServiceImpl = Depends(get_user_service),
):
    try:
        password = hash_password(data.password)
        user = await user_service.create_user(email=data.email, full_name=data.full_name, hashed_password=password)
        del data.password
    except NotFoundError as not_found_error:
        raise not_found_error
    except ConflictError as conflict_error:
        raise conflict_error
    except Exception as e:
        raise InternalServerError(message=str(e))

    return {
        "message": "User created successfully",
        "data": user,
    }
