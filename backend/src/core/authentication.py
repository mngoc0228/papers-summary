import jwt
from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.config import settings, Settings
from src.core.handle_exception import UnauthorizedError

SETTINGS: Settings = settings


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = False):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if credentials.scheme.lower() != "bearer":
                raise UnauthorizedError(message="Invalid authentication scheme.")
            
            data = self.verify_jwt(credentials.credentials)
            
            if data is None:
                raise UnauthorizedError(message="Invalid token or expired token.")
            
            sub = data.get("sub")
            role = data.get("is_admin")

            if sub is None:
                raise UnauthorizedError(message="Invalid token payload.")

            return sub, role
        else:
            raise UnauthorizedError(message="Invalid authorization code.")

    def verify_jwt(self, token: str):
        try:
            payload = jwt.decode(token, SETTINGS.JWT_SECRET_KEY, algorithms=SETTINGS.ALGORITHM)
            if not payload:
                return None
            
            sub = payload.get("sub")
            role = payload.get("is_admin")

            return {"sub": sub, "role": role}
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
