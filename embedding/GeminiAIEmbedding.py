from typing import List
from embedding.EmbeddingService import EmbeddingService
from functools import lru_cache  # For caching


class GeminiAIEmbeddingService(EmbeddingService):
    def __init__(self, model_name="text-embedding-ada-002"):
        self.model_name = model_name

    @lru_cache(maxsize=1024)  # Cache up to 1024 embeddings
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generates an embedding for the provided text using Gemini AI and Vertex AI.

        Args:
            text: The text for which to generate the embedding.

        Returns:
            A list of floats representing the embedding.
        """

        # Import Vertex AI libraries within the function to avoid circular dependencies
        from google.cloud import aiplatform
        from google.cloud.aiplatform.gapic.schema import predict

        # Set Vertex AI project and location (replace with your actual values)
        project = "YOUR_PROJECT_ID"
        location = "us-central1"

        # Set Vertex AI endpoint ID (replace with your actual endpoint ID)
        endpoint_id = "YOUR_ENDPOINT_ID"

        # Create Vertex AI prediction client
        client = aiplatform.gapic.PredictionServiceClient()

        # Prepare prediction request
        instances = [{"text": text}]
        parameters = predict.ExplainRequest.Params(
            feature_attributions=True,
            output_nodes={"embeddings": {"node_ids": ["embeddings"]}}
        )
        request = predict.ExplainRequest(
            endpoint=f"projects/{project}/locations/{location}/endpoints/{endpoint_id}",
            instances=instances,
            parameters=parameters
        )

        # Send prediction request and handle potential errors
        try:
            response = client.explain(request=request)
            return response.explanations[0].attributions["embeddings"].values[0]
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return []  # Return empty list on error

    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        return [self.generate_embedding(text) for text in texts]
