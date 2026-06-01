
export type Job = {
  id: number;
  title: string;
  description: string;
  required_skills: string[];
  
  min_years_experience: number | null;
  location: string | null;
  job_type: string | null;
}


export type BestJob = {
  job_id: number
  title: string
  description: string
  location: string | null
  job_type: string | null
  
  overall_score: number | null 
  text_score: number | null 
  skills_score: number | null
  recommendation: string | null 
}
