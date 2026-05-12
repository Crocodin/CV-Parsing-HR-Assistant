from fastapi import APIRouter, UploadFile, HTTPException

from app.services.extractor import CVExtractor
from app.services.ollama import ollama_service

route = APIRouter()

@route.post("/upload-cv")
async def upload_cv(file: UploadFile):
    file_bytes = await file.read()
    try:        
        text = CVExtractor.extract_text(file_bytes)
        mergered_json = ollama_service.generate_json_for_cv(text)
        
        return {"status" : "ok", "merged_json": mergered_json}
    except ValueError as e:
        # in case of unknown files
        raise HTTPException(status_code=400, detail=str(e))