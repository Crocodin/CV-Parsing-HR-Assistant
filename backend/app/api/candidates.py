from celery.result import AsyncResult
from fastapi import APIRouter, UploadFile, HTTPException, Depends
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.repositories.best import get_best_jobs_for_candidate
from app.services.extractor import CVExtractor
from app.workers.tasks import process_cv
from app.repositories.candidate_repository import CandidateRepository, CandidateEmbeddingRepository
from app.db.session import get_db
from sqlalchemy.orm import Session

route = APIRouter()

@route.get("/all")
async def get_all_candidates(db: Session = Depends(get_db)):
    repo = CandidateRepository(db)
    return repo.get_all_candidates()


class CandidateShell(BaseModel):
    id: int
    name: str

@route.get("/all/shell", response_model=list[CandidateShell])
async def get_all_candidates_shell(db: Session = Depends(get_db)):
    repo = CandidateRepository(db)
    return repo.get_all_candidates_shell()


@route.post("/extract-text")
async def extract_text(file: UploadFile):
    file_bytes = await file.read()
    try:
        text = CVExtractor.extract_text(file_bytes)
        return {"text": text}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@route.get("/{candidate_id}")
async def get_candidate(candidate_id: int, db: Session = Depends(get_db)):
    repo = CandidateRepository(db)
    candidate = repo.get_candidate_by_id(candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate
    

@route.post("/upload-cv")
async def upload_cv(file: UploadFile):
    file_bytes = await file.read()

    try:
        CVExtractor.what_is_file_type(file_bytes)

        task = process_cv.delay(file_bytes)
        return { "status": "processing", "task_id": task.id }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@route.get("/status/{task_id}")
async def cv_status(task_id: str):
    task = AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": task.status,
    }


@route.get("/{candidate_id}/best-jobs")
async def get_best_jobs(candidate_id: int, limit: int = 5, db: Session = Depends(get_db)):
    """ Get the best N jobs for a candidate based on match scores. """
    repo = CandidateRepository(db)
    candidate = repo.get_candidate_by_id(candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    best_jobs = get_best_jobs_for_candidate(candidate_id, db, limit)
    if not best_jobs:
        raise HTTPException(status_code=404, detail="No matching jobs found. Scoring may not be complete.")
    return {"jobs": best_jobs}