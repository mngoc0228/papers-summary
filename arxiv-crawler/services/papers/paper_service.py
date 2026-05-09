import logging

from sqlalchemy.engine import Engine
from sqlmodel import Session, col, select
from services.genai.google_genai import GoogleGenAIService
from models.paper import PaperModel

class PaperService:
    def __init__(self, database_connection: Engine, google_genai_service: GoogleGenAIService | None = None):
        self.google_genai_service = google_genai_service
        self.database_connection = database_connection

    async def summarize_paper(self, paper_content: str) -> str:
        try:
            data = self.google_genai_service.summarize_text(paper_content) if self.google_genai_service else ""
            return data
        except Exception as e:
            logging.error(f"Error summarizing paper: {e}")
            raise e

    async def find_papers_by_titles(self, titles: list[str]):
        try:
            session = Session(self.database_connection)
            statement = select(PaperModel).where(col(PaperModel.title).in_(titles))
            results = session.exec(statement).all()
            papers = [paper for paper in results]

            return papers
        except Exception as e:
            logging.error(f"Error finding papers by titles: {e}")
            raise e
