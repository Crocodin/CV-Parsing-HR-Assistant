from sqlalchemy.orm import Session
import numpy as np


from app.models.embedded_objects import (
    CandidateEmbedding,
    JobDescriptionEmbedding
)


from app.models.raw_objects import MatchResult

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )


def score_candidate(db: Session, candidate_id: int, job_id: int):

    candidate = db.query(CandidateEmbedding).filter(
        CandidateEmbedding.candidate_id == candidate_id
    ).first()

    job = db.query(JobDescriptionEmbedding).filter(
        JobDescriptionEmbedding.job_description_id == job_id
    ).first()

    if not candidate or not job:
        raise ValueError("Candidate or Job not found")

    desc_score = cosine_similarity(
        candidate.description_embedding,
        job.description_embedding
    )

    skills_score = cosine_similarity(
        candidate.skills_embedding,
        job.skills_embedding
    )

    overall = (desc_score * 0.6) + (skills_score * 0.4)

    if overall > 0.8:
        recommendation = "Excellent match"
    elif overall > 0.6:
        recommendation = "Good fit"
    elif overall > 0.4:
        recommendation = "Possible fit"
    else:
        recommendation = "Low match"

    match = MatchResult(
        candidate_id=candidate_id,
        job_description_id=job_id,
        text_score=float(desc_score),
        skills_score=float(skills_score),
        overall_score=float(overall),
        recommendation=recommendation
    )

    db.add(match)
    db.commit()

    return {
        "description_score": float(desc_score),
        "skills_score": float(skills_score),
        "overall_score": float(overall),
        "recommendation": recommendation
    }