import { useEffect, useState } from 'react';
import './App.scss'
import ViewEmbeddings from './components/ViewEmbeddings';
import type { CVPoint2D } from './model/CVPoint2D';
import type { JobPoint2D } from './model/JobPoint2D';
import EmbeddingAPI from './api/EmbeddingAPI';
import CandidateAPI from './api/CandidateAPI';
import CandidateView from './components/CandidateView';
import type { CV } from './model/CV';
import JobView from './components/JobView';
import type { Job } from './model/Job';
import JobAPI from './api/JobAPI';

function App() {
  const [cvPoints, setCvPoints] = useState<CVPoint2D[]>([]);
  const [jobPoints, setJobPoints] = useState<JobPoint2D[]>([]);
  const [loadingPoints, setLoadingPoints] = useState(true);
  const [window, setWindow] = useState<string>("home");

  const [candidatesShell, setCandidatesShell] = useState<CV[]> ([]);
  const [jobsShell, setJobsShell] = useState<Job[]> ([]); 

  useEffect(() => {
    EmbeddingAPI.getAllPoints()
      .then((data) => {
        setCvPoints(data.candidate_points);
        setJobPoints(data.job_points);
      })
      .catch((err) => console.error(err))
      .finally(() => setLoadingPoints(false));
      console.log("Fetched points:", {cvPoints, jobPoints});

    // fetch candidates shell data
    CandidateAPI.getAllCandidates()
      .then((data) => {
        setCandidatesShell(data);
        console.log("Fetched candidates shell data:", data);
      })
      .catch((err) => console.error('Error fetching candidates shell data:', err));
    // fetch jobs shell data
    JobAPI.getAllJobs()
      .then((data) => {
        setJobsShell(data);
        console.log("Fetched jobs shells", jobsShell)
      })
      .catch((err) => console.error('Error fetching jobs shell data:', err))
  }, []);

  if (loadingPoints) return (
    <div className="loading-container">
      <svg className="spinner" width="65px" height="65px" viewBox="0 0 66 66" xmlns="http://www.w3.org/2000/svg">
        <circle className="path" fill="none" strokeWidth="6" strokeLinecap="round" cx="33" cy="33" r="30"></circle>
      </svg>
    </div>
  );

  return (
    <>
      <h1 className="title"><span>H</span>oney badge<span>R</span></h1>
      <div className="options">
        <button className="option-button rounded-sm"
          onClick={() => setWindow("candidates")}
        >Candidates</button>
        <button className="option-button rounded-sm"
          onClick={() => setWindow("jobs")}
        >Jobs</button>
        <button className="option-button rounded-sm"
          onClick={() => setWindow("map")}
        >Map</button>
      </div>

      {window === "home" && (
        <div className="home-container">
          <h2>Welcome to Honey badgeR!</h2>
          <p>Your AI-powered HR assistant for smarter hiring decisions.</p>
        </div>
      )}

      {window === "jobs" && (
        <JobView jobs={jobsShell} jobsUpdated={setJobsShell} />
      )}

      {window === "candidates" && (
        <CandidateView cv={candidatesShell} cvUpdated={setCandidatesShell}/>
      )}

      {window === "map" && (
        <ViewEmbeddings jobData={jobPoints} cvData={cvPoints}/>
      )}
    </>
  );
}

export default App
