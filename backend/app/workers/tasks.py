from celery import Celery

from app.config.config import config
from app.db.session import SessionLocal

from app.models.shell_objects import CandidateCreate
from app.models.embedded_objects import JobDescriptionEmbedding
from app.models.embedded_objects import CandidateEmbedding

from app.repositories.job_repository import jobRepository, jobEmbeddingRepository
from app.repositories.match_repository import matchRepository
from app.repositories.candidate_repository import candidateRepository, candidateEmbeddingRepository

from app.services.extractor import CVExtractor
from app.services.ollama import ollama_service
from app.services.embeddings import embedding_service
from app.services.scorer import cosine_similarity
from app.services.recommender import recommender_service
from app.services.splitter import clean_skills
from app.services.umap_points import compute_umap_points

celery_app = Celery('tasks', broker=config.REDIS_URL, backend=config.REDIS_URL)
celery_app.conf.task_track_started = True

@celery_app.task
def process_cv(file_bytes: bytes, cv_file_path: str = None):
    text = CVExtractor.extract_text(file_bytes)
    # text to json
    merged_json = ollama_service.generate_json_for_cv(text)
    raw_skills = merged_json.get("skills", [])
    # clean skills (remove duplicates, filter out irrelevant ones)
    cleaned_skills_list = clean_skills(raw_skills)
    cleaned_skills_text = ", ".join(cleaned_skills_list)

    personal = merged_json.get("personal", {})
    candidate_data = CandidateCreate(
        name=personal.get("name", "Unknown"),
        email=personal.get("email"),
        phone=personal.get("phone"),
        linkedin=personal.get("linkedin"),
        summary=merged_json.get("summary", ""),
        skills=cleaned_skills_list,
        experience=merged_json.get("experience", []),
        education=merged_json.get("education", []),
        certifications=merged_json.get("certifications", []),
        languages=merged_json.get("languages", []),
        projects=merged_json.get("projects", []),
        achievements=merged_json.get("achievements", []),
        publications=merged_json.get("publications", []),
        cv_file_path=cv_file_path
    )

    candidate = candidateRepository.add_candidate(candidate_data)

    # build description text
    experience_text = " ".join([
        f"{e.get('job_title', '')} at {e.get('company', '')}: {e.get('description', '')}"
        for e in merged_json.get("experience", [])
    ])
    projects_text = " ".join([
        f"{p.get('name', '')}: {p.get('description', '')}"
        for p in merged_json.get("projects", [])
    ])
    description_text = f"{merged_json.get('summary', '')} {experience_text} {projects_text}"

    embedding_service.generate_for_candidate(
        candidate_id=candidate.id,
        description_text=description_text,
        skills_text=cleaned_skills_text
    )

    candidate.status = "DONE"
    return {"candidate_id": candidate.id, "status": "DONE"}


@celery_app.task
def score_candidate_task(candidate_id: int, job_id: int):
    db = SessionLocal()
    try:
        candidate_emb: CandidateEmbedding = candidateEmbeddingRepository.get_candidate_embedding_by_candidate_id(candidate_id)
        job_emb: JobDescriptionEmbedding = jobEmbeddingRepository.get_job_embedding_by_job_id(job_id)

        if not candidate_emb or not job_emb:
            raise ValueError("Embeddings not found")

        text_score = cosine_similarity(
            candidate_emb.description_embedding,
            job_emb.description_embedding
        )
        skills_score = cosine_similarity(
            candidate_emb.skills_embedding,
            job_emb.skills_embedding
        )

        overall = (text_score * 0.6) + (skills_score * 0.4)

        recommendation = recommender_service.generate(
            candidate_id=candidate_id,
            job_id=job_id,
            overall_score=overall,
            db=db
        )

        matchRepository.update_or_add_match(
            candidate_id=candidate_id,
            job_id=job_id,
            text_score=text_score,
            skills_score=skills_score,
            overall=overall,
            recommendation=recommendation
        )
        return {"overall_score": float(overall), "recommendation": recommendation}

    except Exception as e:
        db.rollback()
        print(f"Error scoring candidate: {e}")
        raise

    finally:
        db.close()

@celery_app.task
def compute_umap():
    db = SessionLocal()
    try:
        candidates = db.query(CandidateEmbedding).all()
        jobs = jobEmbeddingRepository.get_all_job_embeddings()

        candidate_embeddings_desc = [c.skills_embedding for c in candidates]

        job_embeddings_desc = [j.skills_embedding for j in jobs]

        # compute umap points for description embeddings
        desc_points = compute_umap_points(candidate_embeddings_desc, job_embeddings_desc)

        # update candidate embeddings with new points
        for i, candidate in enumerate(candidates):
            candidate.point_2D = desc_points["candidate_points"][i]  # or skills_points, depending on which you want to use
            db.add(candidate)

        # update job embeddings with new points
        for j, job in enumerate(jobs):
            job.point_2D = desc_points["job_points"][j]  # or skills_points, depending on which you want to use
            db.add(job)

        db.commit()
        return {"status": "done", "candidates": len(candidates), "jobs": len(jobs)}

    except Exception as e:
        db.rollback()
        print(f"Error computing UMAP points: {e}")
        raise

    finally:
        db.close()

@celery_app.task
def create_job_embedding(job_id: int):
    db = SessionLocal()
    try:
        job = jobRepository.get_job_by_id(job_id)
        if not job:
            raise ValueError("Job not found")

        jobEmbeddingRepository.add_job_embedding(
            job_id=job_id,
            description_embedding=embedding_service.generate(job.description),
            skills_embedding=embedding_service.generate(" ".join(job.required_skills))
        )

        return {"status": "embedding created", "job_id": job_id}
    finally:
        db.close()

