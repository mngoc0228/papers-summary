import jwt
from datetime import timedelta, datetime
from typing import Tuple

from sqlmodel import Session, select

from src.database.models.user import UserModel
from src.dependencies import get_settings
from src.utils.security import verify_password

SETTINGS = get_settings()

class AuthServiceImpl():
    def __init__(self, connection: Session):
        self.connection: Session = connection

    
    async def authenticate(self, email: str, password: str) -> dict | None:
        db_user = await self.get_user_by_email(email=email)
        if not db_user:
            return None
        verified = verify_password(password, db_user.hashed_password)
        if not verified:
            return None
        
        # Generate JWT token
        access_token = self.create_access_token(db_user)

        return {
            "access_token": access_token,
        }
    
    async def get_user_by_email(self, email: str) -> UserModel | None:
        statement = select(UserModel).where(UserModel.email == email)
        session_user = self.connection.exec(statement).first()
        return session_user
    
    async def get_current_user(self, sub: str) -> UserModel | None:
        if not sub:
            return None 
        
        existed_user = await self.get_user_by_email(sub)
        if not existed_user:
            return None
        
        return existed_user

    def create_access_token(self, user: UserModel) -> str:
        expire_minutes = SETTINGS.EXPIRE_MINUTES
        lifetime = datetime.utcnow() + timedelta(minutes=expire_minutes)

        access_token = self._create_token(
            token_type="access_token",
            lifetime=lifetime,
            sub=user.email,
            is_admin=user.is_admin,
            display_name=user.full_name,
            user_id=user.id,
        )

        return access_token
    
    @staticmethod
    def _create_token(
        token_type: str,
        lifetime: datetime,
        sub: str,
        is_admin: bool,
        display_name: str | None,
        user_id: str,
    ) -> str:
        payload = {
            "type": token_type,
            "exp": lifetime,
            "iat": datetime.utcnow(),
            "sub": str(sub),
            "is_admin": str(is_admin),
            "display_name": str(display_name),
            "id": str(user_id)
        }
        return jwt.encode(payload, SETTINGS.JWT_SECRET_KEY, algorithm=SETTINGS.ALGORITHM)

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            return jwt.decode(token, SETTINGS.JWT_SECRET_KEY, algorithms=SETTINGS.ALGORITHM)
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None