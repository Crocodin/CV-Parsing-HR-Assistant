from celery.result import AsyncResult

from fastapi import APIRouter, UploadFile, HTTPException

from app.services.extractor import CVExtractor
from app.workers.tasks import process_cv

route = APIRouter()

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
    

@route.get("/cv-status/{task_id}")
async def cv_status(task_id: str):
    task = AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": task.status,
        "result": task.result if task.status == "SUCCESS" else None
    }