from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.raw_objects import JobDescription
from app.models.embedded_objects import JobDescriptionEmbedding
from app.services.embeddings import embedding_service

from app.services.scorer import score_candidate


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_job(
    title: str,
    description: str,
    required_skills: list[str],
    min_years_experience: int,
    location: str,
    job_type: str,
    db: Session = Depends(get_db)
):

    job = JobDescription(
        title=title,
        description=description,
        required_skills=required_skills,
        min_years_experience=min_years_experience,
        location=location,
        job_type=job_type
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    skills_text = " ".join(required_skills)
    description_text = description

    job_embedding = JobDescriptionEmbedding(
        job_description_id=job.id,
        description_embedding=embedding_service.generate(description_text),
        skills_embedding=embedding_service.generate(skills_text)
    )

    db.add(job_embedding)
    db.commit()

    return {"job_id": job.id}


@router.get("/score")
def get_score(
    candidate_id: int,
    job_id: int,
    db: Session = Depends(get_db)
):
    return score_candidate(db, candidate_id, job_id)