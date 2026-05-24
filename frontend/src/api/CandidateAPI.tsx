import type { CV } from "../model/CV";
import type { Task } from "../model/Task";
import api from "./Api";

class CandidateAPI {
  static async getCandidateById(id: number): Promise<CV>{
    const response = await api.get(`/candidate/${id}`);
    return response.data;
  }

  static async getAllCandidates(): Promise<CV[]> {
    const response = await api.get('/candidate/all');
    return response.data;
  }

  static async uploadCV(file: File): Promise<Task> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post('/candidate/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }
}

export default CandidateAPI;