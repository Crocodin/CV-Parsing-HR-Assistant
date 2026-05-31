import api from "./Api";
import type { Job } from "../model/Job";

class JobAPI {
  static async getJobById(id: number): Promise<Job> {
    const response = await api.get<Job>(`/jobs/${id}`);
    return response.data;
  }

  static async getAllJobs(): Promise<Job[]> {
    const response = await api.get<Job[]>('/jobs/all/shell');
    console.log(response.data);
    return response.data;
  }

  static async uploadJob(job: Omit<Job, 'id'>): Promise<string> {
    const response = await api.post<{job_id: string}>('jobs/create', job);
    return response.data.job_id;
  }
}

export default JobAPI;