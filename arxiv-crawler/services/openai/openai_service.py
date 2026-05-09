import logging

from openai import OpenAI


class OpenAIService:
    def __init__(self, api_key = "choose-any-value", base_url = "https://hermes.ai.unturf.com/v1", model = "adamo1139/Hermes-3-Llama-3.1-8B-FP8-Dynamic"):
        self.base_url = base_url
        self.api_key = api_key
        self.model = model

    def generate_content(self, messages, temperature=0.5):
        try:
            client = OpenAI(base_url=self.base_url, api_key=self.api_key)
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"Error generating content: {e}")
            return None
