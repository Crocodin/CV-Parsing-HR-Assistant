from sqlalchemy.orm import Session

from app.models.embedded_objects import CandidateEmbedding
from app.models.raw_objects import Candidate
from app.models.shell_objects import CandidateCreate
from app.services.splitter import clean_skills
from app.db.session import get_db


class CandidateRepository:
    def __init__(self):
        self.db = get_db()
    
    def add_candidate(self, data: CandidateCreate) -> Candidate:
        try:
            _candidate = Candidate(
                **data.model_dump(),
                status="PROCESSING"
            )
            self.db.add(_candidate)
            self.db.commit()
            self.db.refresh(_candidate)
            return _candidate
        except Exception as e:
            self.db.rollback()
            raise e


class CandidateEmbeddingRepository:
    def __init__(self):
        self.db = get_db()

    def add_candidate_embedding(self, candidate_id: int, description_embedding: list[float], skills_embedding: list[float]):
        try:
            candidate_embedding = CandidateEmbedding(
                candidate_id=candidate_id,
                description_embedding=description_embedding,
                skills_embedding=skills_embedding
            )
            self.db.add(candidate_embedding)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

    def get_candidate_embedding_by_candidate_id(self, candidate_id: int):
        try:
            return self.db.query(CandidateEmbedding).filter(CandidateEmbedding.candidate_id == candidate_id).first()
        except Exception as e:
            self.db.rollback()
            raise e

candidateRepository = CandidateRepository()
candidateEmbeddingRepository = CandidateEmbeddingRepository()