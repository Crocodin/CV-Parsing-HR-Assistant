import api from './Api';
import type { CVPoint2D } from '../model/CVPoint2D';
import type { JobPoint2D } from '../model/JobPoint2D';

class EmbeddingAPI {
  static async getAllPoints(): Promise<{candidate_points: CVPoint2D[], job_points: JobPoint2D[]}> {
    console.log("Fetching points from API...");
    const response = await api.get('umap/points');
    return response.data;
  }
}

export default EmbeddingAPI;