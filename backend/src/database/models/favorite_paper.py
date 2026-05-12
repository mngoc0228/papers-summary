import uuid

from sqlmodel import Field, SQLModel


class FavoritePaperModel(SQLModel, table=True):
    __tablename__ = "favorite_papers"

    user_id: uuid.UUID = Field(foreign_key="users.id", index=True, nullable=False, primary_key=True)
    paper_id: uuid.UUID = Field(foreign_key="papers.id", index=True, nullable=False, primary_key=True)