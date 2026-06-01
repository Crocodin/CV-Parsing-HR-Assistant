
from sqlalchemy.orm import Session
from app.models.raw_objects import MatchResult, Candidate, JobDescription
from app.models.shell_objects import BestCandidate, BestJob

def get_best_jobs_for_candidate(candidate_id: int, db: Session, limit: int = 5):
    """
    Get the best N jobs for a candidate based on match results.
    Returns list of jobs with their match scores ordered by overall_score descending.
    """
    
    results = db.query(
        JobDescription.id.label("job_id"),
        JobDescription.title,
        JobDescription.description,
        JobDescription.location,
        JobDescription.job_type,
        MatchResult.overall_score,
        MatchResult.text_score,
        MatchResult.skills_score,
        MatchResult.recommendation
    ).join(
        MatchResult,
        JobDescription.id == MatchResult.job_description_id
    ).filter(
        MatchResult.candidate_id == candidate_id
    ).order_by(
        MatchResult.overall_score.desc()
    ).limit(limit).all()

    return [ BestJob.model_validate(r._mapping) for r in results ]

def get_best_candidates_for_job(job_id: int, db: Session, limit: int = 5):
    """
    Get the best N candidates for a job based on match results.
    Returns list of candidates with their match scores ordered by overall_score descending.
    """

    results = db.query(
        Candidate.id.label("candidate_id"),
        Candidate.name,
        Candidate.email,
        Candidate.phone,
        Candidate.summary,
        MatchResult.overall_score,
        MatchResult.text_score,
        MatchResult.skills_score,
        MatchResult.recommendation
    ).join(
        MatchResult,
        Candidate.id == MatchResult.candidate_id
    ).filter(
        MatchResult.job_description_id == job_id
    ).order_by(
        MatchResult.overall_score.desc()
    ).limit(limit).all()

    return [ BestCandidate.model_validate(r._mapping) for r in results ]