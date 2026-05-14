from celery import Celery

from app.config.config import config
from app.services.ollama import ollama_service
from app.services.extractor import CVExtractor 

from app.services.embeddings import embedding_service
from app.db.session import SessionLocal
from app.models.raw_objects import Candidate
from app.models.embedded_objects import CandidateEmbedding

celery_app = Celery('tasks', broker=config.REDIS_URL, backend=config.REDIS_URL)

@celery_app.task
def process_cv(file_bytes: bytes):
    db = SessionLocal()

    try:
        text = CVExtractor.extract_text(file_bytes)
        merged_json = ollama_service.generate_json_for_cv(text)
        # the rest of the processing will be here,
        # we wil also pass a candidate id in the future to save the result in the database
        
        print(merged_json)
        candidate = Candidate(
            name=merged_json.get("personal", {}).get("name", "Unknown"),
            email=merged_json.get("personal", {}).get("email"),
            phone=merged_json.get("personal", {}).get("phone"),
            linkedin=merged_json.get("personal", {}).get("linkedin"),

            summary=merged_json.get("summary", ""),

            skills=merged_json.get("skills", []),
            experience=merged_json.get("experience", []),
            education=merged_json.get("education", []),
            certifications=merged_json.get("certifications", []),
            languages=merged_json.get("languages", []),
            projects=merged_json.get("projects", []),
            achievements=merged_json.get("achievements", []),
            publications=merged_json.get("publications", []),

            status="DONE"
        )

        db.add(candidate)
        db.commit()
        db.refresh(candidate)

        skills_text = " ".join(merged_json.get("skills", []))
        summary_text = merged_json.get("summary", "")

        skills_embedding = embedding_service.generate(skills_text)
        summary_embedding = embedding_service.generate(summary_text)


        candidate_embedding = CandidateEmbedding(
            candidate_id = candidate.id,
            description_embedding=summary_embedding,
            skills_embedding=skills_embedding
        )
        db.add(candidate_embedding)
        db.commit()

        return merged_json

    finally:
        db.close()