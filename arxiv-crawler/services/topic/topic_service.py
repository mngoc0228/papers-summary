import asyncio
import logging

from sqlalchemy import Engine
from sqlmodel import Session
from models.topic import TopicModel
from models.paper import PaperModel
from services.genai.google_genai import GoogleGenAIService
from services.openai.openai_service import OpenAIService

class TopicService:
    def __init__(self, database_connection: Engine, genai_service : GoogleGenAIService | None = None, openai_service: OpenAIService | None = None):
        self.database_connection = database_connection
        self.genai_service = genai_service
        self.openai_service = openai_service

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
                if self.openai_service:
                    prompt = (
                        "Bạn là một chuyên gia nghiên cứu về khoa học, bạn thường đọc các bài báo trên arXiv và luôn tóm tắt lại bài báo mỗi lần đọc. Hãy đọc phần tóm tắt (Abstract) của bài báo khoa học sau đây và viết lại thành 1 đoạn tổng quan duy nhất bằng tiếng Việt, nêu bật vấn đề, bài toán họ giải quyết, phương pháp và kết quả chính. Trình bày súc tích, dễ hiểu và mở đầu bằng việc viết bằng việc giới thiệu nghiên cứu làm gì và giải quyết gì, tiếp đến là phương pháp, cuối cùng là kết quả nghiên cứu. Về format của bài tóm tắt, hãy làm có 3 đoạn mỗi đoạn tương ứng với những mục đã nêu trên. Và đây là abstract của bài báo::\n\n"
                        f"{paper.abstract}"
                    )
                    # 15 RPM on the free tier, so we can only summarize 15 papers per minute
                    # await asyncio.sleep(4)
                    summary = self.openai_service.generate_content(messages=[{"role": "user", "content": prompt}])
                    paper.summary = summary
                paper.topics.append(persistent_topic)
                session.add(paper)
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
