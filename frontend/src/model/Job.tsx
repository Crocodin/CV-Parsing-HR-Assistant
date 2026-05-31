
export type Job = {
  id: number;
  title: string;
  description: string;
  required_skills: string[];
  
  min_years_experience: number | null;
  location: string | null;
  job_type: string | null;
}