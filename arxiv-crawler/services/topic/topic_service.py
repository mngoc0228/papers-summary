import asyncio
import logging

from sqlalchemy import Engine
from sqlmodel import Session
from models.topic import TopicModel
from models.paper import PaperModel
from services.genai.google_genai import GoogleGenAIService

class TopicService:
    def __init__(self, database_connection: Engine, genai_service : GoogleGenAIService | None = None):
        self.database_connection = database_connection
        self.genai_service = genai_service

    async def create_topics(self, topics: list[TopicModel]) -> list[TopicModel]:
        created_topics = []
        try:
            session = Session(self.database_connection)
            for topic in topics:
                session.add(topic)
            session.commit()
            for topic in topics:
                session.refresh(topic)
                created_topics.append(topic)

            return created_topics
        except Exception as e:
            logging.error(f"Error creating topic: {e}")
            return None
        finally:
            session.close()
    
    async def create_papers_via_topic(self, topic: TopicModel, papers: list[PaperModel]):
        try:
            session = Session(self.database_connection)
            persistent_topic = session.get(TopicModel, topic.id)
            if persistent_topic is None:
                raise ValueError(f"Topic {topic.id} does not exist in the current session")
            for paper in papers:
                if self.genai_service:
                    prompt = (
                        "Bạn là một chuyên gia về Khoa học Máy tính và AI. Hãy đọc phần tóm tắt (Abstract) "
                        "của bài báo khoa học sau đây và viết lại thành 1 đoạn tổng quan duy nhất bằng tiếng Việt, "
                        "nêu bật bài toán họ giải quyết và phương pháp/kết quả chính. Trình bày súc tích, dễ hiểu:\n\n"
                        f"{paper.abstract}"
                    )
                    # 15 RPM on the free tier, so we can only summarize 15 papers per minute
                    await asyncio.sleep(4)
                    summary = await self.genai_service.summarize_text(prompt)
                    paper.summary = summary
                paper.topics.append(persistent_topic)
                session.add(paper)
                break
            session.commit()
        except Exception as e:
            logging.error(f"Error creating papers for topic: {e}")
            return None
        finally:
            session.close()
    
    async def is_topic_exists(self) -> bool:
        try:
            session = Session(self.database_connection)
            topic = session.query(TopicModel).first()
            return topic is not None
        except Exception as e:
            logging.error(f"Error checking topic existence: {e}")
            return False
        finally:            
            session.close()

    async def get_all_topics(self) -> list[TopicModel]:
        try:
            session = Session(self.database_connection)
            topics = session.query(TopicModel).all()
            return topics
        except Exception as e:
            logging.error(f"Error fetching all topics: {e}")
            return None
        finally:
            session.close()
