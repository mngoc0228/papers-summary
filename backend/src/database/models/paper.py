import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Column
from sqlalchemy.types import JSON
from sqlmodel import Field, Relationship, SQLModel

from src.database.models.topic_paper_link import TopicPaperLinkModel
from src.database.models.favorite_paper import FavoritePaperModel

if TYPE_CHECKING:
    from src.database.models.topic import TopicModel
    from src.database.models.user import UserModel



class PaperModel(SQLModel, table=True):
    __tablename__ = "papers"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field()
    abstract: str = Field()
    authors: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    published_date: str = Field()
    url: str = Field()
    summary: str = Field(default="", nullable=True)

    topics: list["TopicModel"] = Relationship(back_populates="papers", link_model=TopicPaperLinkModel)

    favorite_users: list["UserModel"] = Relationship(back_populates="favorite_papers", link_model=FavoritePaperModel)

    def get_authors_str(self) -> str:
        return ", ".join(self.authors)
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "title": self.title,
            "abstract": self.abstract,
            "authors": self.authors,
            "published_date": self.published_date,
            "url": self.url,
            "summary": self.summary,
            "topics": [topic.to_dict() for topic in self.topics]
        }
