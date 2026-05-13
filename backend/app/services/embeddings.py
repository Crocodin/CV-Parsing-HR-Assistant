import ollama
from app.config.config import config

class EmbeddingService:
    def __init__(self):
        self.client = ollama.Client(config.OLLAMA_URL)
        self.model = config.OLLAMA_EMBEDDING_MODEL


    def generate(self, text: str):
        response = self.client.embeddings(
            model=self.model,
            prompt=text
        )
        return response["embedding"]


embedding_service = EmbeddingService()