import type { CV } from "../model/CV";
import type { BestJob } from "../model/Job";
import { useState, useEffect } from "react";
import CandidateAPI from "../api/CandidateAPI";
import './CandidateView.scss';
import JobAPI from "../api/JobAPI";

function CandidateView({cv, cvUpdated} : {cv: CV[], cvUpdated: (updatedCv: CV[]) => void}) {
  const [clickedCandidate, setClickedCandidate] = useState<CV | null>(null);
  const [candidate, setCandidate] = useState<CV | null>(null);
  const [bestJobs, setBestJobs] = useState<BestJob[]>([]);

  useEffect(() => {
    if (clickedCandidate) {
      CandidateAPI.getCandidateById(clickedCandidate.id)
        .then((cv) => {
          console.log("Fetched candidate details:", cv);
          setCandidate(cv);
        })
        .catch((error) => {
          console.error('Error fetching candidate details:', error);
        });
    } else {
      setCandidate(null);
    }
  }, [clickedCandidate]);

  useEffect(() => {
    if (!clickedCandidate) return;
    const fetchBestJobs = async () => {
      const data = await JobAPI.getBestJobsForCandidate(clickedCandidate.id);
      setBestJobs(data);
    };

    fetchBestJobs();
  }, [clickedCandidate]);

  const pollTaskStatus = (taskId: string) => {
    const intervalId = setInterval(() => {
      CandidateAPI.getTaskStatus(taskId)
        .then((task) => {
          console.log("Polled task status:", task);
          if (task.status === "SUCCESS") {
            clearInterval(intervalId);
            // refetch candidates shell data to update the list with the new candidate
            CandidateAPI.getAllCandidates()
              .then((data) => {
                cvUpdated(data);
                console.log("Re-fetched candidates shell data:", data);
              })
              .catch((err) => console.error('Error refetching candidates shell data:', err));
          } else if (task.status === "FAILED") {
            clearInterval(intervalId);
            console.error('Task failed:', task);
          }
        })
        .catch((error) => {
          clearInterval(intervalId);
          console.error('Error polling task status:', error);
        });
    }, 5000); // poll every 5 seconds
  }

  const handleUpload = async (file: File) => {
    // upload to FastAPI with the saved path
    CandidateAPI.uploadCV(file)
      .then((task) => pollTaskStatus(task.task_id))
      .catch((err) => console.error(err))
  }

  return (
    <div className="main-container">
      {/* candidate names and upload screen */}
      <div className="left">
        <div className="upload-container">
          <h2 onClick={ () =>
            setClickedCandidate(null)
          } >Upload CV</h2>
        </div>
        <div className="sidebar">
          <ul className="candidates">
            {cv.map((candidate) => (
              <li key={candidate.id} className="candidate-card" onClick={
                () => setClickedCandidate(candidate)
              }>
                <h3>{candidate.name ? candidate.name : "Name not available"}</h3>
              </li>
            ))}
          </ul>
        </div>
      </div>
      {/* candidate cv */}
      <div className="right">
        {clickedCandidate === null && (
          <div className="upload-button-container">
            <input type="file" id="cv-upload" style={{ display: 'none' }} accept=".pdf,.doc,.docx" onChange={(e) => {
              const file = e.target.files?.[0]
              if (!file) return;
              handleUpload(file);
              alert("CV uploaded successfully! It may take a few moments to process. Please check back later to see the details.");
            }}/>
            <label htmlFor="cv-upload" className="upload-button rounded-sm">
              Upload CV
            </label>
          </div>
        )}
        {candidate !== null && (
          <div className="cv-details">
            <div className="personal-info">
              <h1 className="name">{ candidate.name ? candidate.name : "Name not available" }</h1>
              <p> {candidate.email ? candidate.email : "Email not available"} | {candidate.phone ? candidate.phone : "Phone not available"}</p>
            </div>
            <ul className="skills">
              {candidate.skills.map((skill, index) => (
                <li className="skill rounded-sm" key={index}>{skill}</li>
              ))}
            </ul>
            <div className="summary">
              {candidate.summary ? candidate.summary : "Summary not available"}
            </div>
            <div className="best-jobs">
              <h2>Best Job Matches</h2>
              <ul className="jobs">
                {bestJobs.map((job) => (
                  <li key={job.job_id} className="job-card">
                    <h3>{job.title ? job.title : "Title not available"}</h3>
                    <p>{job.location ? job.location : "Location not available"} | {job.job_type ? job.job_type : "Job type not available"}</p>
                    <p>Overall Score: {job.overall_score !== null ? job.overall_score.toFixed(2) : "N/A"}</p>
                    <p>Recommendation: {job.recommendation ? job.recommendation : "No recommendation available"}</p>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default CandidateView;