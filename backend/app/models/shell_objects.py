from pydantic import BaseModel

class JobCreate(BaseModel):
    title: str
    description: str
    required_skills: list[str]
    min_years_experience: int
    location: str
    job_type: str