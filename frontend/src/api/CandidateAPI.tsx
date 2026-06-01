import type { BestCandidate, CV } from "../model/CV";
import type { Task } from "../model/Task";
import api from "./Api";

class CandidateAPI {
  static async getCandidateById(id: number): Promise<CV>{
    const response = await api.get(`/candidate/${id}`);
    return response.data;
  }

  static async getAllCandidates(): Promise<CV[]> {
    const response = await api.get('/candidate/all/shell');
    return response.data;
  }

  static async uploadCV(file: File): Promise<Task> {
    const formData = new FormData();
    formData.append('file', file);

    formData.append("file", file);

    const response = await api.post('/candidate/upload-cv', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }

  static async getTaskStatus(taskId: string): Promise<Task> {
    const response = await api.get(`/candidate/status/${taskId}`);
    return response.data;
  }

  static async getBestCandidatesForJob(jobId: number): Promise<BestCandidate[]> {
    const response = await api.get<any>(`/jobs/${jobId}/best-candidates`);
    return response.data.candidates;
  }
}

export default CandidateAPI;