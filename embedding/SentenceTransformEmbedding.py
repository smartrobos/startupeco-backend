from typing import List
from tenacity import retry, stop_after_attempt, wait_exponential
import logging
from embedding.EmbeddingService import EmbeddingService


class SentenceTransformEmbedding(EmbeddingService):

    def __init__(self, model_name="all-mpnet-base-v2"):
        self.model_name = model_name
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(self.model_name)  # Load the model on initialization
        except Exception as error:
            logging.error(f"Error Creating model: {error}", exc_info=True)
            raise error  # Re-raise the exception after logging

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def generate_embedding(self, text: str) -> List[float]:
        # Input validation
        if not text.strip():
            raise ValueError("Input text cannot be empty")

        try:
            embedding = self.model.encode(text)  # Generate the embedding
            return embedding.tolist()  # Convert to list of floats
        except Exception as error:
            logging.error(f"Error generating embedding: {error}", exc_info=True)
            raise error  # Re-raise the exception after logging


if __name__ == '__main__':
    embedding_service = SentenceTransformEmbedding()  # Or specify a different model_name
    text_to_embed = "This is some text to generate an embedding for."
    embedding = embedding_service.generate_embedding(text_to_embed)
    print(f"text for Embedding : {text_to_embed}")
    print(f"Length of Embedding : {len(embedding)}")
    print(f"Embedding : \n{embedding}")  # Output the embedding
