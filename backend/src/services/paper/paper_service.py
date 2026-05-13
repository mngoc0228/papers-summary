from sqlmodel import Session, col, func, select

from src.database.models.user import UserModel
from src.core.base_response import CustomParams
from src.database.models.paper import PaperModel
from fastapi_pagination import Page

from src.database.models.topic import TopicModel


class PaperServiceImpl:
    def __init__(self, connection: Session):
        self.connection: Session = connection

    async def get_papers(self, q: str = None, topic_id: str = None, page: int = 1, size: int = 50) -> Page[PaperModel]:
        try:
            count_statement = (select(func.count()).select_from(PaperModel))
            statement = (
                select(PaperModel).order_by(col(PaperModel.published_date).desc()).offset((page - 1) * size).limit(size)
            )

            if q:
                count_statement = count_statement.where(PaperModel.title.ilike(f"%{q}%"))
                statement = statement.where(PaperModel.title.ilike(f"%{q}%"))

            if topic_id:
                count_statement = (count_statement.join(PaperModel.topics).where(col(TopicModel.id) == topic_id))
                statement = (statement.join(PaperModel.topics).where(col(TopicModel.id) == topic_id))

            count = self.connection.exec(count_statement).one()
            papers = self.connection.exec(statement).all()

            return Page.create(
                items= [paper.to_dict() for paper in papers],
                params=CustomParams(page=page, size=size),
                total=count
            )
        except Exception as e:
            raise e

    async def get_paper_by_id(self, id: str) -> PaperModel | None:
        try:
            statement = select(PaperModel).where(PaperModel.id == id)
            paper = self.connection.exec(statement).one_or_none()
            return paper.to_dict() if paper else None
        except Exception as e:
            raise e

    async def get_papers_by_topic_id(self, topic_id: str, page: int = 1, size: int = 50) -> Page[PaperModel]:
        try:
            count_statement = (
                select(func.count())
                .select_from(PaperModel)
                .join(PaperModel.topics)
                .where(col(TopicModel.id) == topic_id)
            )
            count = self.connection.exec(count_statement).one()

            statement = (
                select(PaperModel)
                .join(PaperModel.topics)
                .where(col(TopicModel.id) == topic_id)
                .order_by(col(PaperModel.published_date).desc())
                .offset((page - 1) * size)
                .limit(size)
            )
            papers = self.connection.exec(statement).all()

            return Page.create(
                items=[paper.to_dict() for paper in papers],
                params=CustomParams(page=page, size=size),
                total=count
            )
        except Exception as e:
            raise e
        
    async def add_favorite_paper(self, user_id: str, paper_id: str) -> None:
        try:
            paper = self.connection.get(PaperModel, paper_id)
            if not paper:
                raise ValueError("Paper not found")

            user = self.connection.get(UserModel, user_id)
            if not user:
                raise ValueError("User not found")

            if paper in user.favorite_papers:
                return

            user.favorite_papers.append(paper)
            self.connection.add(user)
            self.connection.commit()
        except Exception as e:
            raise e

    async def remove_favorite_paper(self, user_id: str, paper_id: str) -> None:
        try:
            paper = self.connection.get(PaperModel, paper_id)
            if not paper:
                raise ValueError("Paper not found")

            user = self.connection.get(UserModel, user_id)
            if not user:
                raise ValueError("User not found")

            if paper not in user.favorite_papers:
                return

            user.favorite_papers.remove(paper)
            self.connection.add(user)
            self.connection.commit()
        except Exception as e:
            raise e
        
    async def get_favorite_papers_by_user_id(self, user_id: str, page: int = 1, size: int = 50) -> Page[PaperModel]:
        try:
            count_statement = (
                select(func.count())
                .select_from(PaperModel)
                .join(PaperModel.favorite_users)
                .where(col(UserModel.id) == user_id)
            )
            count = self.connection.exec(count_statement).one()

            statement = (
                select(PaperModel)
                .join(PaperModel.favorite_users)
                .where(col(UserModel.id) == user_id)
                .order_by(col(PaperModel.published_date).desc())
                .offset((page - 1) * size)
                .limit(size)
            )
            papers = self.connection.exec(statement).all()

            return Page.create(
                items=[paper.to_dict() for paper in papers],
                params=CustomParams(page=page, size=size),
                total=count
            )
        except Exception as e:
            raise e
