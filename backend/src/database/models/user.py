from datetime import datetime
from typing import TYPE_CHECKING
import uuid

from pydantic import EmailStr
from sqlalchemy import DateTime
from sqlmodel import Field, Relationship, SQLModel

from src.utils.util import get_datetime_utc
from src.database.models.follow_topic import FollowTopicModel

if TYPE_CHECKING:
    from src.database.models.follow_topic import FollowTopicModel


class UserModel(SQLModel, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_admin: bool = False
    full_name: str | None = Field(default=None, max_length=255)
    hashed_password: str
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),
    )
    avatar: str | None = Field(default=None, max_length=255)

    topics: list["FollowTopicModel"] = Relationship(back_populates="user", link_model=FollowTopicModel, cascade_delete=True)

    def to_dict(self):
        return {
            "id": str(self.id),
            "email": self.email,
            "is_admin": self.is_admin,
            "full_name": self.full_name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "avatar": self.avatar,
        }
