from fastapi import APIRouter, Depends
from celery.result import AsyncResult
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.embedded_objects import CandidateEmbedding, JobDescriptionEmbedding
from app.workers.tasks import compute_umap, celery_app

router = APIRouter()

@router.get("/compute")
def compute_points():
    compute_umap()
    return { "status": "ok" }

#it returns the status of the umap
@router.get("/status/{task_id}")
def umap_status(task_id: str):
    task = AsyncResult(task_id, app=celery_app)  # force it
    print(f"Backend: {task.backend}")
    print(f"App: {task.app}")
    return {
        "task_id": task_id,
        "status": task.status,
    }

#it gets all the umap points 
@router.get("/points")
def get_all_umap_points(db: Session = Depends(get_db)):
    compute_umap()  # trigger the computation of points if not already done

    candidate_points = db.query(CandidateEmbedding.candidate_id, CandidateEmbedding.point_2D)\
        .filter(CandidateEmbedding.point_2D != None).all()
    job_points = db.query(JobDescriptionEmbedding.job_description_id, JobDescriptionEmbedding.point_2D)\
        .filter(JobDescriptionEmbedding.point_2D != None).all()

    return {
        "candidate_points": [{"id": cp[0], "x": float(cp[1][0]), "y": float(cp[1][1]), "type": "cv"} for cp in candidate_points],
        "job_points": [{"id": jp[0], "x": float(jp[1][0]), "y": float(jp[1][1]), "type": "job"} for jp in job_points]
    }

#it gets the umap points for a candidate and job
@router.get("/points/{candidate_id}/{job_id}")
def get_umap_points(candidate_id: int, job_id: int, db: Session = Depends(get_db)):
    candidate_point = db.query(CandidateEmbedding.point_2D).filter(CandidateEmbedding.candidate_id == candidate_id).first()
    job_point = db.query(JobDescriptionEmbedding.point_2D).filter(JobDescriptionEmbedding.job_description_id == job_id).first()

    return {
        "candidate_point": {"id": candidate_id, "x": float(candidate_point[0]), "y": float(candidate_point[1]), "type": "cv"} if candidate_point else None,
        "job_point": {"id": job_id, "x": float(job_point[0]), "y": float(job_point[1]), "type": "job"} if job_point else None
    }
    