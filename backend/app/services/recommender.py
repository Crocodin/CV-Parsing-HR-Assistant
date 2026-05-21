from sqlalchemy.orm import Session
from app.models.raw_objects import Candidate, JobDescription
from app.services.ollama import ollama_service

class RecommenderService:
    def generate(self, candidate_id: int, job_id: int, overall_score: float, db: Session) -> str:
        candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
        job = db.query(JobDescription).filter(JobDescription.id == job_id).first()

        prompt = f"""
            You are an HR assistant. A candidate has been matched to a job with a score of {overall_score:.0%}.
            
            CANDIDATE SKILLS: {', '.join(candidate.skills or [])}
            CANDIDATE SUMMARY: {candidate.summary}
            
            JOB TITLE: {job.title}
            JOB REQUIRED SKILLS: {', '.join(job.required_skills or [])}
            JOB DESCRIPTION: {job.description}
            
            Write a brief 3-4 sentence HR recommendation explaining:
            1. Why this candidate matches or doesn't match
            2. Key strengths for this role
            3. Any gaps to address
            4. One suggested interview question
            
            BE CONCISE AND FACTUAL. DO NOT INVENT INFORMATION.
        """
        return ollama_service.generate_response(prompt)

recommender_service = RecommenderService()