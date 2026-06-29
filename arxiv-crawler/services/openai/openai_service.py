import logging
from google import genai

class OpenAIService:
    def __init__(self, 
                 api_key = "change_this_to_your_actual_api_key", 
                 base_url = None, 
                 model = None):
        self.client = genai.Client(api_key=api_key)

    def generate_content(self, messages, temperature=0.5):
        try:
            prompt_content = messages[-1]["content"] if messages else ""
            response = self.client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=prompt_content
            )
            return response.text
        except Exception as e:
            logging.error(f"Error generating content: {e}")
            return None
