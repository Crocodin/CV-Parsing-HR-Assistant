from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from celery.result import AsyncResult

from app.db.session import get_db
from app.models.raw_objects import MatchResult
from app.workers.tasks import score_candidate_task

router = APIRouter()

@router.post("/{candidate_id}/{job_id}/trigger")
def trigger_scoring(candidate_id: int, job_id: int):
    task = score_candidate_task.delay(candidate_id, job_id)
    return {"task_id": task.id, "status": "processing"}

@router.get("/status/{task_id}")
def score_status(task_id: str):
    task = AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": task.status,
    }

@router.get("/{candidate_id}/{job_id}")
def get_score(candidate_id: int, job_id: int, db: Session = Depends(get_db)):
    score = db.query(MatchResult).filter(
        MatchResult.candidate_id == candidate_id,
        MatchResult.job_description_id == job_id
    ).first()

    if not score:
        raise HTTPException(status_code=404, detail="Score not found, trigger scoring first")
    return score
