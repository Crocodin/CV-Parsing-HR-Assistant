
export type CVPoint2D = {
  x: number;
  y: number;

  id: number;
  type: 'cv' | 'job';
  name: string;
  score: number;
};