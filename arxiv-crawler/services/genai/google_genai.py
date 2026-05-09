import logging

from google import genai
from google.genai.types import GenerateContentResponse

class GoogleGenAIService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = genai.Client(api_key=api_key)

    async def summarize_text(self, content: str) -> str:
        try:
            logging.info("Summarizing text with Google GenAI")
            response: GenerateContentResponse = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=content
            )

            logging.info("Text summarized successfully with Google GenAI")
            return response.text
        except Exception as e:
            logging.error(f"Error summarizing text with Google GenAI: {e}")
            return ""