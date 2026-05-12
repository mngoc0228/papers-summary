import uuid

from fastapi_pagination import Page
from sqlmodel import Session, func, select

from src.core.base_response import CustomParams
from src.database.models.user import UserModel
from src.database.models.topic import TopicModel


class TopicServiceImpl:
    def __init__(self, connection: Session):
        self.connection: Session = connection

    async def get_topics(self) -> list[TopicModel]:
        try:
            statement = select(TopicModel)
            topics = self.connection.exec(statement).all()
            return [topic.to_dict() for topic in topics]
        except Exception as e:
            raise e

    async def get_topic_by_id(self, id: str) -> TopicModel | None:
        try:
            statement = select(TopicModel).where(TopicModel.id == id)
            topic = self.connection.exec(statement).first()
            return topic.to_dict() if topic else None
        except Exception as e:
            raise e

    async def follow_topic(self, user_id: str, topic_id: str) -> None:
        try:
            topic = self.connection.get(TopicModel, topic_id)
            user = self.connection.get(UserModel, user_id)
            if topic and user not in topic.followers:
                topic.followers.append(user)
                self.connection.add(topic)
                self.connection.commit()
            return {
                "message": "Followed the topic successfully"
            }
        except Exception as e:
            raise e

    async def unfollow_topic(self, user_id: str, topic_id: str) -> None:
        try:
            topic = self.connection.get(TopicModel, topic_id)
            user = self.connection.get(UserModel, user_id)
            if topic and user in topic.followers:
                topic.followers.remove(user)
                self.connection.add(topic)
                self.connection.commit()
            return {
                "message": "Unfollowed the topic successfully"
            }
        except Exception as e:
            raise e

    async def get_followed_topics(self, user_id: str, page: int = 1, size: int = 50) -> Page[TopicModel]:
        try:
            count_statement = (
                select(func.count())
                .select_from(TopicModel)
                .join(TopicModel.followers)
                .where(UserModel.id == user_id)
            )
            total = self.connection.exec(count_statement).one()
            statement = (
                select(TopicModel)
                .join(TopicModel.followers)
                .where(UserModel.id == user_id)
                .order_by(TopicModel.name.asc())
                .offset((page - 1) * size)
                .limit(size)
            )
            topics = self.connection.exec(statement).all()
            return Page.create(
                items=[topic.to_dict() for topic in topics],
                total=total,
                params=CustomParams(page=page, size=size)
            )
        except Exception as e:
            raise e