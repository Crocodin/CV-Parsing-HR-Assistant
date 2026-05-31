import ollama

from app.config.config import config
from app.repositories.job_repository import jobEmbeddingRepository, JobEmbeddingRepository
from app.repositories.candidate_repository import candidateEmbeddingRepository, CandidateEmbeddingRepository

class EmbeddingService:
    def __init__(self, jdr: JobEmbeddingRepository, cdr: CandidateEmbeddingRepository):
        self.client = ollama.Client(config.OLLAMA_URL)
        self.model = config.OLLAMA_EMBEDDING_MODEL
        self.candidate_embedding_repository = cdr
        self.job_embedding_repository = jdr


    def generate(self, text: str):
        response = self.client.embeddings(
            model=self.model,
            prompt=text
        )
        return response["embedding"]
    
    def generate_for_job(self, job_id: int, description_text: str, skills_text: str):
        description_embedding = self.generate(description_text)
        skills_embedding = self.generate(skills_text)
        return self.job_embedding_repository.add_job_embedding(job_id, description_embedding, skills_embedding)
    
    def generate_for_candidate(self, candidate_id: int, description_text: str, skills_text: str):
        description_embedding = self.generate(description_text)
        skills_embedding = self.generate(skills_text)
        return self.candidate_embedding_repository.add_candidate_embedding(candidate_id, description_embedding, skills_embedding)

embedding_service = EmbeddingService(jobEmbeddingRepository, candidateEmbeddingRepository)