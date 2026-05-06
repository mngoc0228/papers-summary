"""
    Dependencies which can be used for DI
"""

from src.dependencies import DBSessionDep
from src.services.auth.auth_service import AuthServiceImpl
from src.services.user.user_service import UserServiceImpl


def get_auth_service(
    database: DBSessionDep,
) -> AuthServiceImpl:
    return AuthServiceImpl(database)

def get_user_service(
    database: DBSessionDep,
) -> UserServiceImpl:
    return UserServiceImpl(database)