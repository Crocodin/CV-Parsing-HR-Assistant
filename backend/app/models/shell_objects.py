from pydantic import BaseModel

class JobCreate(BaseModel):
    title: str
    description: str
    required_skills: list[str]
    min_years_experience: int
    location: str
    job_type: str

class CandidateCreate(BaseModel):
    name: str
    email: str | None = None
    phone: str | None = None
    linkedin: str | None = None
    summary: str = ""
    skills: list[str] = []
    experience: list[dict] = []
    education: list[dict] = []
    certifications: list[dict] = []
    languages: list[str] = []
    projects: list[dict] = []
    achievements: list[dict] = []
    publications: list[dict] = []
    cv_file_path: str | None = None

class BestCandidate(BaseModel):
    candidate_id: int
    name: str
    email: str | None = None
    phone: str | None = None
    summary: str = ""
    overall_score: float | None = None
    text_score: float | None = None
    skills_score: float | None = None
    recommendation: str | None = None

class BestJob(BaseModel):
    job_id: int
    title: str
    description: str
    location: str
    job_type: str
    overall_score: float | None = None
    text_score: float | None = None
    skills_score: float | None = None
    recommendation: str | None = None