from celery.result import AsyncResult
from fastapi import APIRouter, Depends, UploadFile, HTTPException
from sqlalchemy.orm import Session

from app.services.extractor import CVExtractor
from app.workers.tasks import process_cv
from app.db.session import get_db
from app.models.raw_objects import Candidate

route = APIRouter()

@route.get("/all")
async def get_all_candidates(db: Session = Depends(get_db)):
    candidates = db.query(Candidate).all()
    return candidates

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
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate
    

@route.post("/upload-cv")
async def upload_cv(file: UploadFile):
    file_bytes = await file.read()
    try:        
        CVExtractor.what_is_file_type(file_bytes)  # this will raise an error if the file type is unknown
        
        task = process_cv.delay(file_bytes)

        return { "status": "processing", "task_id": task.id }
    except ValueError as e:
        # in case of unknown files
        raise HTTPException(status_code=400, detail=str(e))
    

@route.get("/status/{task_id}")
async def cv_status(task_id: str):
    task = AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": task.status,
        "result": task.result if task.status == "SUCCESS" else None
    }