import logging

from services.genai.google_genai import GoogleGenAIService

class PaperService:
    def __init__(self, google_genai_service: GoogleGenAIService, app_context):
        self.google_genai_service = google_genai_service
        self.app_context = app_context

    async def summarize_paper(self, paper_content: str) -> str:
        try:
            data = self.google_genai_service.summarize_text(paper_content)
            return data
        except Exception as e:
            logging.error(f"Error summarizing paper: {e}")
            raise
    
    async def save_paper(self, paper_data):
        # Implement logic to save paper data to the database using app_context
        pass
