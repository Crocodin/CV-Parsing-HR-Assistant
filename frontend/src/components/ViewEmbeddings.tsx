import EmbeddingCanvas from "./EmbeddingCanvas";
import './ViewEmbeddings.scss';
import type { JobPoint2D } from "../model/JobPoint2D";
import type { CVPoint2D } from "../model/CVPoint2D";
import { useEffect, useState } from "react";
import type { CV } from "../model/CV";
import CandidateAPI from "../api/CandidateAPI";
import type { Job } from "../model/Job";
import JobAPI from "../api/JobAPI";

function distance(point1: {x: number, y: number}, point2: {x: number, y: number}): number {
  return Math.sqrt(Math.pow(point1.x - point2.x, 2) + Math.pow(point1.y - point2.y, 2));
}

function getProcentageDistance(point1: {x: number, y: number}, point2: {x: number, y: number}): number {
  const dist = distance(point1, point2);
  if (dist === 0) return 100;
  const maxDist = Math.sqrt(Math.pow(200, 2) + Math.pow(200, 2)); // max distance in the canvas
  return Math.max(0, 100 - (dist / maxDist) * 100);
}

function ViewEmbeddings({jobData, cvData} : {jobData : JobPoint2D[], cvData: CVPoint2D[]}) {
  const [selectedPoint, setSelectedPoint] = useState<JobPoint2D | CVPoint2D | null>(null);

  const [selectedCV, setSelectedCV] = useState<CV | null>(null);
  const [loadingCV, setLoadingCV] = useState(false);

  const [closestJobPoint, setClosestJobPoint] = useState<JobPoint2D | null>(null);
  const [furthestJobPoint, setFurthestJobPoint] = useState<JobPoint2D | null>(null);

  const [closestJob, setClosestJob] = useState<Job | null>(null);
  const [furthestJob, setFurthestJob] = useState<Job | null>(null);

  const [selectedJob, setSelectedJob] = useState<Job | null>(null);
  const [loadingJob, setLoadingJob] = useState(false);

  useEffect(() => {
    if (selectedPoint && selectedPoint.type === 'cv') {
      setLoadingCV(true);
      setSelectedCV(null);
      CandidateAPI.getCandidateById(selectedPoint.id)
        .then((cv) => setSelectedCV(cv))
        .catch((error) => {
          console.error('Error fetching CV details:', error);
        })
        .finally(() => {
          setLoadingCV(false);
          setSelectedJob(null);
          setSelectedJob(null);
        });

      // now, for all the job points, we want to calculate the distance to the selected CV point and log it
      const { closestJobPoint, furthestJobPoint } = jobData.reduce((acc, curr) => {
        const dist = distance(selectedPoint, curr);
        return {
          closestJobPoint:  dist < distance(selectedPoint, acc.closestJobPoint)  ? curr : acc.closestJobPoint,
          furthestJobPoint: dist > distance(selectedPoint, acc.furthestJobPoint) ? curr : acc.furthestJobPoint,
        };
      }, { closestJobPoint: jobData[0], furthestJobPoint: jobData[0] });

      setClosestJobPoint(closestJobPoint);
      setFurthestJobPoint(furthestJobPoint);

      JobAPI.getJobById(closestJobPoint.id)
        .then((job) => setClosestJob(job))
        .catch((error) => {
          console.error('Error fetching closest job details:', error);
        });

      JobAPI.getJobById(furthestJobPoint.id)
        .then((job) => setFurthestJob(job))
        .catch((error) => {
          console.error('Error fetching furthest job details:', error);
        });
    } if (selectedPoint && selectedPoint.type === 'job') {
        setLoadingJob(true);
        setSelectedJob(null);
        JobAPI.getJobById(selectedPoint.id)
          .then((job) => setSelectedJob(job))
          .catch((error) => {
            console.error('Error fetching job details:', error);
          })
          .finally(() => {
            setLoadingJob(false);
            setSelectedCV(null);
            setClosestJobPoint(null);
            setFurthestJobPoint(null);
            setClosestJob(null);
            setFurthestJob(null);
          });
    } else {
      setSelectedCV(null);
      setClosestJobPoint(null);
      setFurthestJobPoint(null);
      setClosestJob(null);
      setFurthestJob(null);
    }
  }, [selectedPoint]);

  return (
    <div className="view-embeddings">
      <div className="embedding-details rounded-lg">
        <h2>Details</h2>
        {loadingCV ? (
          <p>Loading CV details...</p>
        ) : selectedCV ? (
          <div className="cv-details">
            <div className="personal-info">
              <h3>{selectedCV.name}</h3>
              <p>{selectedCV.email} | {selectedCV.phone}</p>
            </div>

            <div className="devider"/>
            <ul className="skills">
              {selectedCV.skills.map((skill, index) => (
                <li className="skill rounded-sm" key={index}>{skill}</li>
              ))}
            </ul>
            
            <div className="summary">
              <p>{selectedCV.summary}</p>
            </div>

            <div className="job-distances">
              {closestJobPoint && selectedPoint && (
                <p>{closestJob?.title || 'Closest job'}: {getProcentageDistance(closestJobPoint, selectedPoint).toFixed(2)}%</p>
              )}
              {furthestJobPoint && selectedPoint && (
                <p>{furthestJob?.title || 'Furthest job'}: {getProcentageDistance(furthestJobPoint, selectedPoint).toFixed(2)}%</p>
              )}
            </div>

            <button className="view-cv-button rounded-sm" onClick={() => window.open(selectedCV.cv_file_path || '#', '_blank')}>
              View CV
            </button>
          </div>
        ) : null }
        { loadingJob ? (
          <p>Loading job details...</p>
        ) : selectedJob ? (
          <div className="job-details">
            <h3>{selectedJob.title}</h3>
            
            <ul className="skills">
              {selectedJob.required_skills.map((skill, index) => (
                <li className="skill rounded-sm" key={index}>{skill}</li>
              ))}
            </ul>

            <p>{selectedJob.description}</p>
          </div>
        ) : null }
      </div>
      <EmbeddingCanvas data={[...jobData, ...cvData]} setSelectedPoint={setSelectedPoint} />
    </div>
  );
}

export default ViewEmbeddings;