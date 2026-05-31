from sqlalchemy.orm import Session
from app.models.raw_objects import MatchResult
from app.db.session import get_db

class MatchRepository:
    def __init__(self):
        self.db = get_db()

    def update_or_add_match(self, candidate_id: int, job_id: int, text_score: float, skills_score: float, overall: float, recommendation: str):
        try:
            match = self.db.query(MatchResult).filter(
                MatchResult.candidate_id == candidate_id,
                MatchResult.job_description_id == job_id
            ).first()
            if match:
                match.text_score = text_score
                match.skills_score = skills_score
                match.overall_score = overall
                match.recommendation = recommendation
                self.db.commit()
            else:
                match = MatchResult(
                    candidate_id=candidate_id,
                    job_description_id=job_id,
                    text_score=text_score,
                    skills_score=skills_score,
                    overall_score=overall,
                    recommendation=recommendation
                )
                self.db.add(match)
                self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
            
matchRepository = MatchRepository()