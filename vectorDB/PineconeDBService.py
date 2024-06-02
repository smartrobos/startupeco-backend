import pinecone
from typing import List
from vectorDB.VectorDBService import VectorDBService


class PineconeDBService(VectorDBService):
    def __init__(self, api_key, environment, index_name):
        pinecone.init(api_key=api_key, environment=environment)
        self.index = pinecone.Index(index_name)
    
    def upsert_embedding(self, profile_id: str, embedding: List[float]):
        self.index.upsert([(profile_id, embedding)])
    
    def query_embedding(self, embedding: List[float], top_k: int = 5):
        return self.index.query(embedding, top_k=top_k, include_metadata=True)
