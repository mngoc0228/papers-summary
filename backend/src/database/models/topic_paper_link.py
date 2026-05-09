import uuid

from sqlmodel import Field, SQLModel


class TopicPaperLinkModel(SQLModel, table=True):
    __tablename__ = "paper_topics"

    paper_id: uuid.UUID = Field(foreign_key="papers.id", primary_key=True, default=None)
    topic_id: uuid.UUID = Field(foreign_key="topics.id", primary_key=True, default=None)