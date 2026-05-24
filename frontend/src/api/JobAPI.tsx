import api from "./Api";
import type { Job } from "../model/Job";

class JobAPI {
  static async getJobById(id: number): Promise<Job> {
    const response = await api.get(`/jobs/${id}`);
    return response.data;
  }

  static async getAllJobs(): Promise<Job[]> {
    const response = await api.get('/jobs/all');
    return response.data;
  }
}

export default JobAPI;