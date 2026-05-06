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
            role = data.get("role")

            if sub is None or role is None:
                raise UnauthorizedError(message="Invalid token payload.")

            return sub, role
        else:
            raise UnauthorizedError(message="Invalid authorization code.")

    def verify_jwt(self, token: str):
        try:
            # Decode token
            payload = jwt.decode(token, SETTINGS.jwt_secret_key, algorithms=SETTINGS.algorithm)
            if not payload:
                return None
            
            sub = payload.get("sub")
            role = payload.get("role")

            #TODO: Check if token is active
            # if not self._is_active_token(role, sub, token):
            #     return None
                
            return {"sub": sub, "role": role}
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

