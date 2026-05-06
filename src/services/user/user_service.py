
from sqlmodel import Session, select

from src.database.models.user import User
from src.dependencies import get_settings


SETTINGS = get_settings()

class UserServiceImpl():
    def __init__(self, connection: Session):
        self.connection: Session = connection
        
    async def get_user_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        session_user = self.connection.exec(statement).first()
        return session_user

    async def create_user(self, email: str, hashed_password: str, full_name: str | None = None, is_admin = False) -> User:
        # Check if user with the same email already exists
        existing_user = await self.get_user_by_email(email)
        if existing_user:
            raise Exception("User with this email already exists")

        new_user = User(
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            is_admin=is_admin,
        )
        self.connection.add(new_user)
        self.connection.commit()
        self.connection.refresh(new_user)
        return new_user
