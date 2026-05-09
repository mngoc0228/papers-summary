from sqlmodel import Session, select

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
