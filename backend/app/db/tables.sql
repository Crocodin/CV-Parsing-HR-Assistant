-- the actual tables are made by alembic migrations, but this is the source of truth for the schema, and also useful for raw SQL queries when needed

CREATE TABLE candidates (
    -- basic info
    id SERIAL PRIMARY KEY,
    name TEXT,
    email TEXT,
    phone TEXT,
    linkedin TEXT,
    summary TEXT,

    -- technical details
    skills TEXT[],
    experience JSONB,
    education JSONB,
    certifications JSONB,
    languages TEXT[],
    projects JSONB,
    achievements JSONB,
    publications JSONB,

    -- celery task tracking
    status TEXT DEFAULT 'pending',
    task_id TEXT,

    -- file tracking
    cv_file_path TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE job_descriptions (
    id SERIAL PRIMARY KEY,
    title TEXT,

    -- job details
    description TEXT,
    required_skills TEXT[],

    -- useful for filtering before even running embeddings
    min_years_experience INTEGER,
    location TEXT,
    job_type TEXT, -- full-time, part-time, internship

    -- file tracking
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE EXTENSION IF NOT EXISTS vector;

-- the main thinq we will compare is the description of the job vs candidate  summary + experience descriptions + projects descriptions, and the joined skills of the job vs candidate
CREATE TABLE candidate_embeddings (
    id SERIAL PRIMARY KEY,
    candidate_id INTEGER REFERENCES candidates(id) ON DELETE CASCADE,
    description_embedding VECTOR(768), 
    skills_joined_embedding VECTOR(768),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE job_embeddings (
    id SERIAL PRIMARY KEY,
    job_id INTEGER REFERENCES job_descriptions(id) ON DELETE CASCADE,
    description_embedding VECTOR(768),
    skills_joined_embedding VECTOR(768),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE match_scores (
    id SERIAL PRIMARY KEY,
    candidate_id INTEGER REFERENCES candidates(id) ON DELETE CASCADE,
    job_id INTEGER REFERENCES job_descriptions(id) ON DELETE CASCADE,
    
    text_score FLOAT,           -- cosine similarity of descriptions
    skills_score FLOAT,         -- cosine similarity of skills
    final_score FLOAT,          -- weighted combination
    
    recommendation TEXT,        -- qwen's explanation
    
    created_at TIMESTAMP DEFAULT NOW()
);