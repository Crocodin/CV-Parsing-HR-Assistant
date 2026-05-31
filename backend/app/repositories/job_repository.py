from sqlalchemy.orm import Session

from app.models.embedded_objects import JobDescriptionEmbedding
from app.models.raw_objects import JobDescription
from app.models.shell_objects import JobCreate
from app.db.session import get_db

class JobRepository:
    def __init__(self):
        self.db = get_db()

    def add_job(self, job: JobCreate):
        try:
            _job = JobDescription(
                title=job.title,
                description=job.description,
                required_skills=job.required_skills,
                min_years_experience=job.min_years_experience,
                location=job.location,
                job_type=job.job_type,
            )
            self.db.add(_job)
            self.db.commit()
            self.db.refresh(_job)
            return _job
        except Exception as e:
            self.db.rollback()
            raise e

    def get_all_jobs(self):
        try:
            return self.db.query(JobDescription).all()
        except Exception as e:
            self.db.rollback()
            raise e

    def get_job_by_id(self, job_id: int):
        try:
            return self.db.query(JobDescription).filter(JobDescription.id == job_id).first()
        except Exception as e:
            self.db.rollback()
            raise e

    def get_all_jobs_shell(self):
        try:
            jobs = self.db.query(JobDescription.id, JobDescription.title).all()
            return [{"id": j[0], "title": j[1]} for j in jobs]
        except Exception as e:
            self.db.rollback()
            raise e

class JobEmbeddingRepository:
    def __init__(self):
        self.db = get_db()
        
    def add_job_embedding(self, job_id: int, description_embedding: list[float], skills_embedding: list[float]):
        try:
            job_embedding = JobDescriptionEmbedding(
                job_description_id=job_id,
                description_embedding=description_embedding,
                skills_embedding=skills_embedding,
                )
            self.db.add(job_embedding)
            self.db.commit()
            self.db.refresh(job_embedding)
            return job_embedding
        except Exception as e:
            self.db.rollback()
            raise e

    def get_all_job_embeddings(self):
        try:
            return self.db.query(JobDescriptionEmbedding).all()
        except Exception as e:
            self.db.rollback()
            raise e

    def get_job_embedding_by_job_id(self, job_id: int):
        try:
            return self.db.query(JobDescriptionEmbedding).filter(JobDescriptionEmbedding.job_description_id == job_id).first()
        except Exception as e:
            self.db.rollback()
            raise e

jobRepository = JobRepository()
jobEmbeddingRepository = JobEmbeddingRepository()