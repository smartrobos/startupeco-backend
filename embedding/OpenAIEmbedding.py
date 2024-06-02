from typing import List
import logging
from tenacity import retry, stop_after_attempt, wait_exponential
import os
from embedding.EmbeddingService import EmbeddingService


class OpenAIEmbeddingService(EmbeddingService):

    def __init__(self, model_name="text-embedding-ada-002"):
        self.model_name = model_name

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def generate_embedding(self, text: str) -> List[float]:
        # Input validation
        if not text.strip():
            raise ValueError("Input text cannot be empty")

        try:
            import openai
            openai.api_key = os.getenv("OPENAI_API_KEY")
            response = openai.Embedding.create(
                model=self.model_name,
                input=text
            )
            return response['data'][0]['embedding']
        except Exception as error:
            logging.error(f"Error generating embedding: {error}", exc_info=True)
            raise error  # Re-raise the exception after logging
