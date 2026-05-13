from celery import Celery

from app.config.config import config
from app.services.ollama import ollama_service
from app.services.extractor import CVExtractor 

celery_app = Celery('tasks', broker=config.REDIS_URL, backend=config.REDIS_URL)

@celery_app.task
def process_cv(file_bytes: bytes):
    text = CVExtractor.extract_text(file_bytes)
    merged_json = ollama_service.generate_json_for_cv(text)
    # the rest of the processing will be here,
    # we wil also pass a candidate id in the future to save the result in the database
    return merged_json