from fastapi import APIRouter, UploadFile, HTTPException

# this path might be from backend.app.services
from app.services.extractor import CVExtractor

route = APIRouter()

@route.post("/upload-cv")
async def upload_cv(file: UploadFile):
    file_bytes = await file.read()
    extractor = CVExtractor()
    try:        
        text = extractor.extract_text(file_bytes)
        # continue with the spliter and all other steps
        return {"status" : "ok"}
    except ValueError as e:
        # in case of unknown files
        raise HTTPException(status_code=400, detail=str(e))