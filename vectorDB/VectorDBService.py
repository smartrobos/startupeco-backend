from typing import List

class VectorDBService:
    def upsert_embedding(self, profile_id: str, embedding: List[float]):
        raise NotImplementedError

    def query_embedding(self, embedding: List[float], top_k: int = 5):
        raise NotImplementedError