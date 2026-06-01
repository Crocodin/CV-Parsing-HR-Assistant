import ollama

from app.config.config import config
from app.repositories.job_repository import JobEmbeddingRepository
from app.repositories.candidate_repository import CandidateEmbeddingRepository
from sqlalchemy.orm import Session

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
    
    def generate_for_job(self, job_id: int, description_text: str, skills_text: str, db: Session):
        description_embedding = self.generate(description_text)
        skills_embedding = self.generate(skills_text)
        job_embedding_repository = JobEmbeddingRepository(db)
        return job_embedding_repository.add_job_embedding(job_id, description_embedding, skills_embedding)
    
    def generate_for_candidate(self, candidate_id: int, description_text: str, skills_text: str, db: Session = None):
        description_embedding = self.generate(description_text)
        skills_embedding = self.generate(skills_text)
        if db is None:
            from app.db.session import SessionLocal
            db = SessionLocal()
            candidate_embedding_repository = CandidateEmbeddingRepository(db)
            result = candidate_embedding_repository.add_candidate_embedding(candidate_id, description_embedding, skills_embedding)
            db.close()
            return result
        else:
            candidate_embedding_repository = CandidateEmbeddingRepository(db)
            return candidate_embedding_repository.add_candidate_embedding(candidate_id, description_embedding, skills_embedding)

embedding_service = EmbeddingService()