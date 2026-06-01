import { useEffect, useState } from "react";
import type { Job } from "../model/Job";
import JobAPI from "../api/JobAPI";
import './JobView.scss'
import type { BestCandidate } from "../model/CV";
import CandidateAPI from "../api/CandidateAPI";

function JobView({jobs, jobsUpdated} : {jobs: Job[], jobsUpdated: (updatedJob: Job[]) => void}) {
  const [clickedJob, setClickedJob] = useState<Job | null>(null);
  const [fullJob, setFullJob] = useState<Job | null>(null);
  const [bestCandidates, setBestCandidates] = useState<BestCandidate[]>([]);

  useEffect(() => {
    if (!clickedJob) return;

    const fetchFullJob = async () => {
      const data = await JobAPI.getJobById(clickedJob.id);
      setFullJob(data)
    };

    fetchFullJob();
  }, [clickedJob]);

  useEffect(() => {
    if (!clickedJob) return;
    const fetchBestCandidates = async () => {
      const data = await CandidateAPI.getBestCandidatesForJob(clickedJob.id);
      setBestCandidates(data);
    };

    fetchBestCandidates();
  }, [clickedJob]);

  const [jobFormData, setJobFormData] = useState<Omit<Job, 'id'>>({
    title: "",
    description: "",
    required_skills: [],
    min_years_experience: null,
    location: null,
    job_type: null,
  });

  const handleFormChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { id, value } = e.target;
    setJobFormData((prev) => ({...prev, [id]: value}))
  }

  return (
    <div className="main-container">
      {/* job view and upload side */}
      <div className="left">
        <div className="upload-container">
          <h2 onClick={ () => {
            setClickedJob(null);
          }}> Upload CV </h2>
        </div>
        <div className="sidebar">
          <ul className="jobs">
            {jobs.map((job) => (
              <li key={job.id} className="job-card" onClick={
                () => setClickedJob(job)
              }>
                <h3> {job.title ? job.title : "Title not available" } </h3>
              </li>
            ))}
          </ul>
        </div>
      </div>
      {/* job full on view  */}
      <div className="right">
        {/* if no job is clicked we will just have the upload screen */}
        {clickedJob === null && (
          <form className="upload-container">
            <input type="text" id="title" value={jobFormData.title} onChange={handleFormChange} placeholder="Title" />
            <input type="text" id="description" value={jobFormData.description} onChange={handleFormChange} placeholder="Description" />
            <input type="text" id="required_skills" value={jobFormData.required_skills.join(", ")} onChange={ (e) => {
              setJobFormData((prev) => ({...prev, required_skills: e.target.value.split(",").map(s => s.trim())}))
            }} placeholder="Skills (comma separated)"/>
            <input type="text" id="location" value={jobFormData.location ?? ""} onChange={handleFormChange} placeholder="Location" />
            <input type="text" id="job_type" value={jobFormData.job_type ?? ""} onChange={handleFormChange} placeholder="Job type" />
            <input type="number" id="min_years_experience" value={jobFormData.min_years_experience ?? ""} onChange={handleFormChange} placeholder="Min. years experience" />
            <input type="button" value={"Upload Job"} onClick={() => {JobAPI.uploadJob(jobFormData).then(async () => {
              jobsUpdated(await JobAPI.getAllJobs())
            }).catch((err) => {console.error("Error sending job", err)})}}/>
          </form>
        )}
        {/* now here we just show the form data basically */}
        {clickedJob !== null && (
          <div className="job-details">
            <div className="general-info">
              <h1 className="title">{ fullJob?.title ? fullJob.title : "Title not available" }</h1>
              <p className="small-info">
                { fullJob?.location ? fullJob.location : "No location specified"}
                |
                { fullJob?.job_type ? fullJob.job_type : "No type specified"}
              </p>
            </div>
            <ul className="skills">
              {fullJob?.required_skills.map((skill, index) => (
                <li className="skill rounded-sm" key={index}>{skill}</li>
              ))}
            </ul>
            <div className="description">
              {fullJob?.description ? fullJob.description : "Description not available"}
            </div>
            <h2>Best Candidates</h2>
            <ul className="best-candidates">
              {bestCandidates.map((candidate) => (
                <li key={candidate.candidate_id} className="candidate-card">
                  <h3>{candidate.name ? candidate.name : "Name not available"}</h3>
                  <p>{candidate.email ? candidate.email : "Email not available"} | {candidate.phone ? candidate.phone : "Phone not available"}</p>
                  <p>Overall Score: {candidate.overall_score !== null ? candidate.overall_score.toFixed(2) : "N/A"}</p>
                  <p>Recommendation: {candidate.recommendation ? candidate.recommendation : "No recommendation available"}</p>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  )
}

export default JobView