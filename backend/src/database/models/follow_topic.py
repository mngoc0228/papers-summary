from typing import TYPE_CHECKING
import uuid

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.database.models.user import UserModel
    from src.database.models.topic import TopicModel

class FollowTopicModel(SQLModel, table=True):
    __tablename__ = "follow_topics"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True, nullable=False)
    topic_id: uuid.UUID = Field(foreign_key="topics.id", index=True, nullable=False)

    user: "UserModel" = Relationship(back_populates="followed_topics")
    topic: "TopicModel" = Relationship(back_populates="followers")
