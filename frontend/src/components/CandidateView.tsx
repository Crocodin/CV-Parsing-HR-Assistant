import type { CVPoint2D } from "../model/CVPoint2D";
import type { CV } from "../model/CV";
import { useState, useEffect } from "react";
import CandidateAPI from "../api/CandidateAPI";
import './CandidateView.scss';

function CandidateView({cv}: {cv: CVPoint2D[]}) {
  const [clickedCandidate, setClickedCandidate] = useState<CVPoint2D | null>(null);
  const [candidate, setCandidate] = useState<CV | null>(null);

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

  return (
    <div className="main-container">
      {/* the main view of candidate */}
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
      {/* candidate cv and upload section */}
      <div className="right">
        {clickedCandidate === null && (
          <div className="upload-button-container">
            <input type="file" id="cv-upload" style={{ display: 'none' }} accept=".pdf,.doc,.docx"/>
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
            {candidate.cv_file_path ? (
              <iframe
                className="candidate-cv"
                src={candidate.cv_file_path}
                width="100%"
                height="100%"
                title="Candidate CV"
              />
            ) : (
              <div>
                <p>No CV available</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default CandidateView;