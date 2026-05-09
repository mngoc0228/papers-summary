"""
    Dependencies which can be used for DI
"""

from fastapi import Depends

from src.core.authentication import JWTBearer
from src.core.handle_exception import UnauthorizedError
from src.dependencies import DBSessionDep
from src.services.auth.auth_service import AuthServiceImpl
from src.services.topic.topic_service import TopicServiceImpl
from src.services.user.user_service import UserServiceImpl
from src.services.paper.paper_service import PaperServiceImpl


def get_auth_service(
    database: DBSessionDep,
) -> AuthServiceImpl:
    return AuthServiceImpl(database)

def get_user_service(
    database: DBSessionDep,
) -> UserServiceImpl:
    return UserServiceImpl(database)

async def get_current_user(
    auth_service: AuthServiceImpl = Depends(get_auth_service),
    credentials: tuple[str, str] = Depends(JWTBearer())
):
    sub, _ = credentials
    
    user = await auth_service.get_current_user(sub)
    if user is None:
        raise UnauthorizedError(message="Invalid token or expired token.")

    return user


# Paper DI
def get_paper_service(
    database: DBSessionDep,
) -> PaperServiceImpl:
    return PaperServiceImpl(database)

# Topic DI
def get_topic_service(
    database: DBSessionDep,
) -> TopicServiceImpl:
    return TopicServiceImpl(database)
