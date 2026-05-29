from fastapi import APIRouter, Depends
from celery.result import AsyncResult
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.embedded_objects import CandidateEmbedding, JobDescriptionEmbedding
from app.workers.tasks import compute_umap, celery_app
from app.models.raw_objects import Candidate

router = APIRouter()

@router.get("/compute")
def compute_points():
    task = compute_umap.delay()
    return {"status": "processing", "task_id": task.id}

@router.get("/status/{task_id}")
def umap_status(task_id: str):
    task = AsyncResult(task_id, app=celery_app)  # force it
    print(f"Backend: {task.backend}")
    print(f"App: {task.app}")
    return {
        "task_id": task_id,
        "status": task.status,
        "result": task.result if task.status == "SUCCESS" else None
    }

@router.get("/points")
def get_all_umap_points(db: Session = Depends(get_db)):

    candidate_points = (
        db.query(
            Candidate.id,
            Candidate.name,
            CandidateEmbedding.point_2D
        )
        .join(CandidateEmbedding, CandidateEmbedding.candidate_id == Candidate.id)
        .filter(CandidateEmbedding.point_2D.isnot(None))
        .all()
    )

    job_points = (
        db.query(
            JobDescriptionEmbedding.job_description_id,
            JobDescriptionEmbedding.point_2D
        )
        .filter(JobDescriptionEmbedding.point_2D.isnot(None))
        .all()
    )

    return {
        "candidate_points": [
            {
                "id": c[0],
                "name": c[1],
                "x": float(c[2][0]),
                "y": float(c[2][1]),
                "type": "cv"
            }
            for c in candidate_points
        ],
        "job_points": [
            {
                "id": j[0],
                "x": float(j[1][0]),
                "y": float(j[1][1]),
                "type": "job"
            }
            for j in job_points
        ]
    }

@router.get("/points/{candidate_id}/{job_id}")
def get_umap_points(candidate_id: int, job_id: int, db: Session = Depends(get_db)):
    candidate_point = db.query(CandidateEmbedding.point_2D).filter(CandidateEmbedding.candidate_id == candidate_id).first()
    job_point = db.query(JobDescriptionEmbedding.point_2D).filter(JobDescriptionEmbedding.job_description_id == job_id).first()

    return {
        "candidate_point": {"id": candidate_id, "x": float(candidate_point[0]), "y": float(candidate_point[1]), "type": "cv"} if candidate_point else None,
        "job_point": {"id": job_id, "x": float(job_point[0]), "y": float(job_point[1]), "type": "job"} if job_point else None
    }
    