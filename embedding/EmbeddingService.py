from typing import List


class EmbeddingService:
    def generate_embedding(self, text: str) -> List[float]:
        raise NotImplementedError
