from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.raw_objects import JobDescription
from app.models.embedded_objects import JobDescriptionEmbedding
from app.services.embeddings import embedding_service
from app.models.shell_objects import JobCreate


router = APIRouter()

def _create_job_embedding(job_id: int, db: Session = Depends(get_db)):
    print(f"Creating embedding for job {job_id}")
    job = db.query(JobDescription).filter(JobDescription.id == job_id).first()
    if not job:
        raise ValueError("Job not found")
    
    print(f"Generating embeddings for job {job_id}")

    job_embedding = JobDescriptionEmbedding(
        job_description_id=job_id,
        description_embedding=embedding_service.generate(job.description),
        skills_embedding=embedding_service.generate(" ".join(job.required_skills))
    )
    print(f"Saving embeddings for job {job_id}")
    db.add(job_embedding)
    db.commit()

@router.post("/")
def create_job(job_data: JobCreate, db: Session = Depends(get_db)):
    job = JobDescription(
        title=job_data.title,
        description=job_data.description,
        required_skills=job_data.required_skills,
        min_years_experience=job_data.min_years_experience,
        location=job_data.location,
        job_type=job_data.job_type
    )

    db.add(job)
    db.commit()
    db.refresh(job)
    _create_job_embedding(job.id, db)
    return {"job_id": job.id}

@router.post("/{job_id}/trigger")
def create_job_embedding(job_id: int, db: Session = Depends(get_db)):
    _create_job_embedding(job_id, db)
    return {"status": "ok"}