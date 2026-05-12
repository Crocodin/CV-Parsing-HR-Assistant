from fastapi import APIRouter, UploadFile, HTTPException

# this path might be from backend.app.services
from app.services.extractor import CVExtractor
from app.services.splitter import Splitter

route = APIRouter()

@route.post("/upload-cv")
async def upload_cv(file: UploadFile):
    file_bytes = await file.read()
    extractor = CVExtractor()
    splitter = Splitter()
    try:        
        text = extractor.extract_text(file_bytes)
        sections = splitter.split_into_sections(text)
        # this well be contiunted with all the ollama stuff
        return {"status" : "ok", "sections": sections}
    except ValueError as e:
        # in case of unknown files
        raise HTTPException(status_code=400, detail=str(e))