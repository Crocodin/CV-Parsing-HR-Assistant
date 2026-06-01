
export type CV = {
  id: number;
  name: string;
  email: string | null;
  phone: string | null;
  linkedin: string | null;
  summary: string;
  cv_file_path: string | null;

  skills: string[];
  languages: string[];

  experience: {
    job_title: string;
    company: string;
    start: string;
    end: string;
    years_of_experience: number | null;
    description: string;
  }[];

  education: {
    degree: string;
    field_of_study: string;
    institution: string;
    start: string;
    end: string;
  }[];

  certifications: {
    name: string;
    issuing_organization: string;
    date_obtained: string;
    date_expiration: string | null;
  }[];

  achievements: {
    name: string;
    description: string;
    date_obtained: string;
  }[];

  publications: {
    title: string;
    publication_venue: string;
    date_published: string;
  }
}

export type BestCandidate = {
  candidate_id: number;
  name: string;
  email: string | null;
  phone: string | null;
  summary: string;
  overall_score: number | null;
  text_score: number | null;
  skills_score: number | null;
  recommendation: string | null;
}
