import uuid
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from src.database.models.topic_paper_link import TopicPaperLinkModel
from src.database.models.follow_topic import FollowTopicModel
if TYPE_CHECKING:
    from src.database.models.paper import PaperModel
    from src.database.models.user import UserModel


class TopicModel(SQLModel, table=True):
    __tablename__ = "topics"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field()
    code: str = Field()
    description: str = Field(default="", nullable=True)
    papers: list["PaperModel"] = Relationship(back_populates="topics", link_model=TopicPaperLinkModel)
    followers: list["UserModel"] = Relationship(back_populates="followed_topics", link_model=FollowTopicModel)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "name": self.name,
            "code": self.code,
            "description": self.description,
        }
