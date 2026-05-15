from sqlalchemy import Column, Float, Integer, String, Text, DateTime, JSON, ARRAY, func

from app.db.session import Base

class Candidate(Base):
    __tablename__ = "candidates"

    # base info
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    linkedin = Column(String, nullable=True)
    summary = Column(Text)

    # technical details
    skills = Column(ARRAY(String))
    experience = Column(JSON)
    education = Column(JSON)
    certifications = Column(JSON)
    languages = Column(ARRAY(String))
    projects = Column(JSON)
    achievements = Column(JSON)
    publications = Column(JSON)

    # celery task tracking
    processing_task_id = Column(String, unique=True, nullable=True)
    status = Column(String, default="PENDING")

    # file tracking
    cv_file_path = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)

    # job details
    description = Column(Text)
    required_skills = Column(ARRAY(String))

    # minimum requirements
    min_years_experience = Column(Integer)
    location = Column(String)
    job_type = Column(String) # full-time, part-time, internship

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class MatchResult(Base):
    __tablename__ = "match_results"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, nullable=False)
    job_description_id = Column(Integer, nullable=False)

    # the actual match result with scores and explanations
    text_score = Column(Float)
    skills_score = Column(Float)
    overall_score = Column(Float)

    recommendation = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now())