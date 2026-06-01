from app.models.embedded_objects import CandidateEmbedding
from app.models.raw_objects import Candidate
from app.models.shell_objects import CandidateCreate
from sqlalchemy.orm import Session


class CandidateRepository:
    def __init__(self, db: Session):
        self.db = db
    
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
        
    def get_all_candidates(self):
        try:
            return self.db.query(Candidate).all()
        except Exception as e:
            self.db.rollback()
            raise e
        
    def get_candidate_by_id(self, candidate_id: int):
        try:
            return self.db.query(Candidate).filter(Candidate.id == candidate_id).first()
        except Exception as e:
            self.db.rollback()
            raise e
        
    def get_all_candidates_shell(self):
        try:
            candidates = self.db.query(Candidate.id, Candidate.name).all()
            return [{"id": c[0], "name": c[1]} for c in candidates]
        except Exception as e:
            self.db.rollback()
            raise e


class CandidateEmbeddingRepository:
    def __init__(self, db: Session):
        self.db = db

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