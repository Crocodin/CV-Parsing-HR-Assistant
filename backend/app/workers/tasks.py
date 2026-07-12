from celery import Celery

from app.config.config import config
from app.db.session import SessionLocal

from app.models.shell_objects import CandidateCreate
from app.models.embedded_objects import JobDescriptionEmbedding
from app.models.embedded_objects import CandidateEmbedding

from app.repositories.job_repository import JobRepository, JobEmbeddingRepository
from app.repositories.match_repository import MatchRepository
from app.repositories.candidate_repository import CandidateRepository, CandidateEmbeddingRepository

from app.services.extractor import CVExtractor
from app.services.ollama import ollama_service
from app.services.embeddings import embedding_service
from app.services.scorer import cosine_similarity
from app.services.recommender import recommender_service
from app.services.splitter import clean_skills
from app.services.umap_points import compute_umap_points
from app.models.raw_objects import Candidate, JobDescription

celery_app = Celery('tasks', broker=config.REDIS_URL, backend=config.REDIS_URL)
celery_app.conf.task_track_started = True

@celery_app.task
def process_cv(file_bytes: bytes):
    db = SessionLocal()
    try:
        text = CVExtractor.extract_text(file_bytes)
        merged_json = ollama_service.generate_json_for_cv(text)
        raw_skills = merged_json.get("skills", [])
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
            cv_file_path='',
        )

        candidate_repo = CandidateRepository(db)
        candidate = candidate_repo.add_candidate(candidate_data)

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
            skills_text=cleaned_skills_text,
            db=db
        )

        candidate.status = "DONE"

        print(f"Candidate {candidate.id} processed, starting auto-scoring against all jobs...")
        auto_score_candidate_against_all_jobs.delay(candidate.id)
        return {"candidate_id": candidate.id, "status": "DONE"}
    finally:
        db.close()


@celery_app.task
def score_candidate_task(candidate_id: int, job_id: int):
    db = SessionLocal()
    try:
        candidate_emb_repo = CandidateEmbeddingRepository(db)
        candidate_repo = CandidateRepository(db)
        job_emb_repo = JobEmbeddingRepository(db)
        job_repo = JobRepository(db)

        # before we score based on embeddings we will score then based on the minimum requirements the job asked for
        candidate: Candidate = candidate_repo.get_candidate_by_id(candidate_id)
        job: JobDescription = job_repo.get_job_by_id(job_id)

        if not candidate or not job:
            raise ValueError("Candidate or Job not found")
        
        # years of experience
        required_years = job.min_years_experience or 0
        candidate_years = sum(e.get("years_of_experience", 0) for e in candidate.experience)

        if candidate_years < required_years:
            experience_score = candidate_years / required_years
        else:
            experience_score = 1.0

        # skills match
        required_skills = set(job.required_skills or [])
        candidate_skills = set(candidate.skills or [])

        exact_matches = required_skills & candidate_skills

        candidate_emb: CandidateEmbedding = candidate_emb_repo.get_candidate_embedding_by_candidate_id(candidate_id)
        job_emb: JobDescriptionEmbedding = job_emb_repo.get_job_embedding_by_job_id(job_id)

        if not candidate_emb or not job_emb:
            raise ValueError("Embeddings not found")
        
        similarity_score = cosine_similarity(
            candidate_emb.skills_embedding,
            job_emb.skills_embedding
        )
        skills_score = (len(exact_matches) / (len(required_skills) + 1e-5) + (len(candidate_skills) - len(exact_matches)) / (len(required_skills) + 1e-5)) * similarity_score
        
        # description match
        text_score = cosine_similarity(
            candidate_emb.description_embedding,
            job_emb.description_embedding
        )

        overall = (text_score * 0.55) + (skills_score * 0.35) + (experience_score * 0.1)

        recommendation = recommender_service.generate(
            candidate_id=candidate_id,
            job_id=job_id,
            overall_score=overall,
            db=db
        )

        match_repo = MatchRepository(db)
        match_repo.update_or_add_match(
            candidate_id=candidate_id,
            job_id=job_id,
            text_score=text_score,
            skills_score=skills_score,
            experience_score=experience_score,
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


def compute_umap():
    db = SessionLocal()
    try:
        job_emb_repo = JobEmbeddingRepository(db)
        
        candidates = db.query(CandidateEmbedding).all()
        jobs = job_emb_repo.get_all_job_embeddings()

        candidate_embeddings_desc = [c.description_embedding for c in candidates]

        job_embeddings_desc = [j.description_embedding for j in jobs]

        desc_points = compute_umap_points(candidate_embeddings_desc, job_embeddings_desc)

        for i, candidate in enumerate(candidates):
            candidate.point_2D = desc_points["candidate_points"][i]
            db.add(candidate)

        for j, job in enumerate(jobs):
            job.point_2D = desc_points["job_points"][j]
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
        job_repo = JobRepository(db)
        job = job_repo.get_job_by_id(job_id)
        if not job:
            raise ValueError("Job not found")

        job_emb_repo = JobEmbeddingRepository(db)
        job_emb_repo.add_job_embedding(
            job_id=job_id,
            description_embedding=embedding_service.generate(job.description),
            skills_embedding=embedding_service.generate(" ".join(job.required_skills))
        )

        print(f"Job {job_id} embedding created, starting auto-scoring against all candidates...")
        auto_score_job_against_all_candidates.delay(job_id)

        return {"status": "embedding created", "job_id": job_id}
    finally:
        db.close()

@celery_app.task
def auto_score_candidate_against_all_jobs(candidate_id: int):
    """
    Score a new candidate against all existing jobs.
    This is called automatically when a new CV is processed.
    """
    db = SessionLocal()
    try:
        print(f"Candidate {candidate_id} processed, starting auto-scoring against all jobs...")
        job_repo = JobRepository(db)
        jobs = job_repo.get_all_jobs()
        for job in jobs:
            score_candidate_task.delay(candidate_id, job.id)
    except Exception as e:
        print(f"Error auto-scoring candidate {candidate_id}: {e}")
        raise e
    finally:
        db.close()

@celery_app.task
def auto_score_job_against_all_candidates(job_id: int):
    """
    Score a new job against all existing candidates.
    This is called automatically when a new job is created.
    """
    db = SessionLocal()
    try:
        print(f"Job {job_id} embedding created, starting auto-scoring against all candidates...")
        candidate_repo = CandidateRepository(db)
        candidates = candidate_repo.get_all_candidates()
        for candidate in candidates:
            score_candidate_task.delay(candidate.id, job_id)
    except Exception as e:
        print(f"Error auto-scoring job {job_id}: {e}")
        raise e
    finally:
        db.close()
