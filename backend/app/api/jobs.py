from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db.session import get_db
from app.models.raw_objects import JobDescription
from app.models.shell_objects import JobCreate
from app.workers.tasks import create_job_embedding

router = APIRouter()


@router.post("/create")
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
    create_job_embedding.delay(job.id)
    return {"job_id": job.id}

@router.get("/all")
def get_all_jobs(db: Session = Depends(get_db)):
    jobs = db.query(JobDescription).all()
    return jobs

class JobShell(BaseModel):
    id: int
    title: str

@router.get("/all/shell", response_model=list[JobShell])
def get_all_jobs(db: Session = Depends(get_db)):
    jobs = db.query(JobDescription.id, JobDescription.title).all()
    return [{"id": j[0], "title": j[1]} for j in jobs]

@router.get("/{job_id}")
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(JobDescription).filter(JobDescription.id == job_id).first()
    if not job:
        raise ValueError("Job not found")
    return job

@router.post("/{job_id}/trigger")
def trigger_job_embedding(job_id: int, db: Session = Depends(get_db)):
    create_job_embedding.delay(job_id, db)
    return {"status": "ok"}
