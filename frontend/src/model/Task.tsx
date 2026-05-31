
export type Task = {
  status: string;
  task_id: string;
  result: {
    candidate_id: number;
    status: string;
  }
}