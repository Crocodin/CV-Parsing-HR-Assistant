from fastapi import APIRouter
from pydantic import BaseModel

from app.models.shell_objects import JobCreate
from app.workers.tasks import create_job_embedding
from app.repositories.job_repository import jobRepository

router = APIRouter()

@router.post("/create")
def create_job(job_data: JobCreate):
    job = jobRepository.add_job(job_data)
    return {"job_id": job.id}

@router.get("/all")
def get_all_jobs():
    return jobRepository.get_all_jobs()
    
class __JobShell__(BaseModel):
    id: int
    title: str

@router.get("/all/shell", response_model=list[__JobShell__])
def get_all_jobs():
    return jobRepository.get_all_jobs_shell()

@router.get("/{job_id}")
def get_job(job_id: int):
    return jobRepository.get_job_by_id(job_id)

@router.post("/{job_id}/trigger")
def trigger_job_embedding(job_id: int):
    create_job_embedding.delay(job_id)
    return {"status": "ok"}
