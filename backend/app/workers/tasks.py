from celery import Celery
from app.config.config import config
from app.services.extractor import CVExtractor
from app.services.ollama import ollama_service
from app.services.embeddings import embedding_service
from app.services.scorer import cosine_similarity
from app.services.recommender import recommender_service
from app.db.session import SessionLocal
from app.models.raw_objects import Candidate, MatchResult
from app.models.embedded_objects import CandidateEmbedding, JobDescriptionEmbedding
from app.services.splitter import clean_skills
from app.services.umap_points import compute_umap_points

celery_app = Celery('tasks', broker=config.REDIS_URL, backend=config.REDIS_URL)
celery_app.conf.task_track_started = True

@celery_app.task
def process_cv(file_bytes: bytes):
    db = SessionLocal()
    try:
        text = CVExtractor.extract_text(file_bytes)
        # text to json
        merged_json = ollama_service.generate_json_for_cv(text)
        print("Merged JSON:", merged_json)
        raw_skills = merged_json.get("skills", [])
        # clean skills (remove duplicates, filter out irrelevant ones)
        cleaned_skills_list = clean_skills(raw_skills)   # returns list → for DB
        cleaned_skills_text = ", ".join(cleaned_skills_list)

        candidate = Candidate(
            name=merged_json.get("personal", {}).get("name", "Unknown"),
            email=merged_json.get("personal", {}).get("email"),
            phone=merged_json.get("personal", {}).get("phone"),
            linkedin=merged_json.get("personal", {}).get("linkedin"),
            summary=merged_json.get("summary", ""),
            skills=raw_skills,  # save original skills as well
            experience=merged_json.get("experience", []),
            education=merged_json.get("education", []),
            certifications=merged_json.get("certifications", []),
            languages=merged_json.get("languages", []),
            projects=merged_json.get("projects", []),
            achievements=merged_json.get("achievements", []),
            publications=merged_json.get("publications", []),
            status="PROCESSING"
        )
        db.add(candidate)
        db.commit()
        db.refresh(candidate)

        # 4. build description text (summary + experience + projects)
        experience_text = " ".join([
            f"{e.get('job_title', '')} at {e.get('company', '')}: {e.get('description', '')}"
            for e in merged_json.get("experience", [])
        ])
        projects_text = " ".join([
            f"{p.get('name', '')}: {p.get('description', '')}"
            for p in merged_json.get("projects", [])
        ])
        description_text = f"{merged_json.get('summary', '')} {experience_text} {projects_text}"

        description_embedding = embedding_service.generate(description_text)
        print(cleaned_skills_text)
        skills_embedding = embedding_service.generate(cleaned_skills_text)

        # save embeddings
        candidate_embedding = CandidateEmbedding(
            candidate_id=candidate.id,
            description_embedding=description_embedding,
            skills_embedding=skills_embedding
        )
        db.add(candidate_embedding)
        db.commit()

        # mark as DONE
        candidate.status = "DONE"
        db.commit()

        return {"candidate_id": candidate.id, "status": "DONE"}

    except Exception as e:
        db.rollback()
        print(f"Error processing CV: {e}")
        raise
    finally:
        db.close()


@celery_app.task
def score_candidate_task(candidate_id: int, job_id: int):
    db = SessionLocal()
    try:
        candidate_emb = db.query(CandidateEmbedding).filter(
            CandidateEmbedding.candidate_id == candidate_id
        ).first()

        job_emb = db.query(JobDescriptionEmbedding).filter(
            JobDescriptionEmbedding.job_description_id == job_id
        ).first()

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

        # get recommendation from qwen
        recommendation = recommender_service.generate(
            candidate_id=candidate_id,
            job_id=job_id,
            overall_score=overall,
            db=db
        )

        # search for match if it exists
        match = db.query(MatchResult).filter(
            MatchResult.candidate_id == candidate_id,
            MatchResult.job_description_id == job_id 
        ).first()

        if not match:
            match = MatchResult(
                candidate_id = candidate_id,
                job_description_id = job_id,
                text_score = float(text_score),
                skills_score = float(skills_score),
                overall_score = float(overall),
                recommendation = recommendation
            )
            db.add(match)
            db.commit()
        else:
            match.text_score = float(text_score)
            match.skills_score = float(skills_score)
            match.overall_score = float(overall)
            recommendation = recommendation
            db.commit()

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
        jobs = db.query(JobDescriptionEmbedding).all()

        candidate_embeddings_desc = [c.description_embedding for c in candidates]

        job_embeddings_desc = [j.description_embedding for j in jobs]

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

    except Exception as e:
        db.rollback()
        print(f"Error computing UMAP points: {e}")
        raise

    finally:
        db.close()