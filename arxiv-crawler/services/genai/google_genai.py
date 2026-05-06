from google import genai


class GoogleGenAIService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = genai.Client(api_key=api_key)

    def summarize_text(self, content: str) -> str:
        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=content
        )

        return response.json()
