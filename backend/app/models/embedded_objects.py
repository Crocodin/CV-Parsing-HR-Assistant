from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, DateTime, Integer, ForeignKey, func
from app.db.session import Base

class CandidateEmbedding(Base):
    __tablename__ = "candidate_embeddings"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id", ondelete="CASCADE"))
    # for cosine similarity scoring
    description_embedding = Column(Vector(768))
    skills_embedding = Column(Vector(768))

    created_at = Column(DateTime(timezone=True), server_default=func.now())

class JobDescriptionEmbedding(Base):
    __tablename__ = "job_description_embeddings"

    id = Column(Integer, primary_key=True, index=True)
    job_description_id = Column(Integer, ForeignKey("jobs_descriptions.id", ondelete="CASCADE"))
    # for cosine similarity scoring
    description_embedding = Column(Vector(768))
    skills_embedding = Column(Vector(768))

    created_at = Column(DateTime(timezone=True), server_default=func.now())