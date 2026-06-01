from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from app.models.shell_objects import JobCreate
from app.workers.tasks import create_job_embedding
from app.repositories.job_repository import JobRepository, JobEmbeddingRepository
from app.repositories.best import get_best_candidates_for_job
from app.db.session import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/create")
def create_job(job_data: JobCreate, db: Session = Depends(get_db)):
    repo = JobRepository(db)
    job = repo.add_job(job_data)
    create_job_embedding.delay(job.id)
    return {"job_id": job.id}

@router.get("/all")
def get_all_jobs(db: Session = Depends(get_db)):
    repo = JobRepository(db)
    return repo.get_all_jobs()
    
class __JobShell__(BaseModel):
    id: int
    title: str

@router.get("/all/shell", response_model=list[__JobShell__])
def get_all_jobs_shell(db: Session = Depends(get_db)):
    repo = JobRepository(db)
    return repo.get_all_jobs_shell()


@router.post("/{job_id}/trigger")
def trigger_job_embedding(job_id: int):
    create_job_embedding.delay(job_id)
    return {"status": "ok"}

@router.get("/{job_id}/best-candidates")
def get_best_candidates(job_id: int, limit: int = 5, db: Session = Depends(get_db)):
    """
    Get the best N candidates for a job based on match scores.
    """
    repo = JobRepository(db)
    job = repo.get_job_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    best_candidates = get_best_candidates_for_job(job_id, db, limit)
    if not best_candidates:
        raise HTTPException(status_code=404, detail="No matching candidates found. Scoring may not be complete.")
    return {"candidates": best_candidates}

@router.get("/{job_id}")
def get_job(job_id: int, db: Session = Depends(get_db)):
    repo = JobRepository(db)
    return repo.get_job_by_id(job_id)