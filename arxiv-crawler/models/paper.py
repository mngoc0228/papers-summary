import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Column
from sqlalchemy.types import JSON
from sqlmodel import Field, Relationship, SQLModel

from models.topic_paper_link import TopicPaperLinkModel

if TYPE_CHECKING:
    from models.topic import TopicModel


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
        }
