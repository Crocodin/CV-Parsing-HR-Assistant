from fastapi import APIRouter, Depends
from celery.result import AsyncResult
from sqlalchemy.orm import Session
from backend.app.db.session import get_db
from backend.app.models.embedded_objects import CandidateEmbedding, JobDescriptionEmbedding

router = APIRouter()

@router.get("/compute")
def compute_umap():
    task = compute_umap.delay()
    return {"status": "processing", "task_id": task.id}

@router.get("/status/{task_id}")
def umap_status(task_id: str):
    task = AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": task.status,
        "result": task.result if task.status == "SUCCESS" else None
    }

@router.get("/points/{candidate_id}/{job_id}")
def get_umap_points(candidate_id: int, job_id: int, db: Session = Depends(get_db)):
    candidate_point = db.query(CandidateEmbedding.point_2D).filter(CandidateEmbedding.candidate_id == candidate_id).first()
    job_point = db.query(JobDescriptionEmbedding.point_2D).filter(JobDescriptionEmbedding.job_description_id == job_id).first()

    return {
        "candidate_point": candidate_point[0] if candidate_point else None,
        "job_point": job_point[0] if job_point else None
    }
    