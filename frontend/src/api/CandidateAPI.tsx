import type { CV } from "../model/CV";
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

  static async uploadCV(file: File, cv_file_path: string): Promise<Task> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('cv_file_path', cv_file_path);

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
}

export default CandidateAPI;