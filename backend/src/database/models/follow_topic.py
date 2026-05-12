from typing import TYPE_CHECKING
import uuid

from sqlmodel import Field, SQLModel


class FollowTopicModel(SQLModel, table=True):
    __tablename__ = "follow_topics"

    user_id: uuid.UUID = Field(foreign_key="users.id", index=True, nullable=False, primary_key=True)
    topic_id: uuid.UUID = Field(foreign_key="topics.id", index=True, nullable=False, primary_key=True)
