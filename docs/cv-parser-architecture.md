# CV Parser & HR Assistant — Architecture Overview

## Project Summary

An AI-powered desktop application (HoneyBadgeR) that helps HR personnel screen CVs faster and with less bias.
It parses CVs, extracts structured data, compares candidates against job descriptions, generates  
match scores, and provides explainable recommendations. The system supports human decision-making, it does not automate hiring decisions.

Team size: 3 students.

---

## Full Tech Stack

| Layer                           | Technology                           | Optional |
|---------------------------------|--------------------------------------|----------|
| Desktop Frontend                | React (TypeScript)                   | No.      |
| Backend API                     | FastAPI (Python)                     | No.      |
| Database                        | PostgreSQL + pgvector                | No.      |
| Migrations                      | Alembic                              | Yes      |
| Job Queue                       | Redis + Celery                       | Yes      |
| LLM (parsing + recommendations) | Ollama — granite4.1:3b               | No.      |
| Embeddings (scoring)            | Ollama — embeddinggemma:300m         | No.      |
| PDF extraction                  | pdfplumber                           | No.      |
| DOCX extraction                 | python-docx                          | No.      |
| Auth                            | JWT                                  | Yes      |
| Containerization                | Docker Compose (partial — see below) | No.      |


> **Note:** Initial architecture planned for `qwen3.5:4b` and `nomic-embed-text-v2-moe`.
> During development we switched to `granite4.1:3b` (LLM) and `embeddinggemma:300m` (embeddings)
> for better performance on available hardware.

---

## What Runs Where

```
Your Machine (native)
├── Ollama                  -> serves granite4.1:3b and embeddinggemma:300m
│     └── accessible at localhost:11434
└── React frontend          -> talks to FastAPI via HTTP

Docker Compose
├── FastAPI                 -> talks to Ollama at host.docker.internal:11434
├── PostgreSQL              -> data persistence via Docker volume
├── Redis                   -> job queue for Celery
├── Celery worker           -> processes CV parsing jobs
└── pgAdmin                 -> database GUI at localhost:5050
```

React and Ollama run natively on the machine. FastAPI, PostgreSQL, Redis, Celery, and pgAdmin
run inside Docker. No GPU passthrough needed — Ollama has direct access to the GPU as a native process.

---

## CV Processing Pipeline

```
User uploads PDF or DOCX
↓
pdfplumber / python-docx        -> raw text extraction
↓
Celery queue                    -> jobs processed one at a time, Ollama not hammered
↓
granite4.1:3b via Ollama        -> one prompt → structured JSON from full CV text
↓
Assemble final candidate JSON
{ name, email, skills[], experience[], education[] }
↓
PostgreSQL                      -> save candidate + parsed data                      -> save candidate + parsed data
```

> **Note:** An earlier approach used a rule-based section splitter (regex) to divide the CV into
> sections before sending each to the LLM. This was deprecated because pdfplumber does not always
> preserve newlines, making reliable splitting impossible. See `services/splitter.py` and
> `services/merger.py` for the old code, kept for reference.


---

## Matching & Scoring Pipeline

```
Candidate JSON + Job Description JSON
        ↓
embeddinggemma:300m             -> convert both to embedding vectors
        ↓                       (the job description embendings will be cached)
Cosine similarity               -> match score 0–100%
        ↓
PostgreSQL                      -> save score
        ↓
If score > threshold (e.g. 50%)
        ↓
granite4.1:3b via Ollama        -> generate explanation + recommendations
"Candidate matches 78% — strong Python skills, missing Docker.
 Suggested interview question: ..."
        ↓
PostgreSQL                      -> save recommendation text
```

The LLM is only called for explanation on promising candidates, not every CV.
Embeddings handle the fast, automatic scoring pass.

---

## What Gets Stored in PostgreSQL

| Table           | Purpose                                      |
|-----------------|----------------------------------------------|
| users           | HR user accounts (JWT auth)                  |
| job_postings    | Job descriptions uploaded by HR              |
| candidates      | Parsed CV data (structured JSON)             |
| cv_embeddings   | nomic embedding vectors (reused across jobs) |
| match_scores    | Score between a candidate and a job posting  |
| recommendations | LLM explanation text per match               |

Rule: anything expensive to compute gets stored so it is never recomputed.

---

## Key Architectural Decisions

- **No external APIs** — everything runs locally, no costs, no internet dependency
- **Embeddings for scoring, LLM for explanation** — fast semantic matching first, expensive LLM call only when needed
- **Celery queue** — prevents Ollama from being hammered when multiple CVs are uploaded at once
- **Alembic** — database schema changes tracked like code, no manual SQL alterations
- **pgvector** — PostgreSQL extension for storing and querying embedding vectors natively
---

## What the HR Dashboard Shows (HoneyBadgeR)

The app has three views, switchable from the top navigation:

- **Candidates** — list of parsed CVs, click to see extracted skills, experience, education,
  match score, and AI-generated recommendation
- **Jobs** — list of uploaded job descriptions, upload new ones
- **Map** — UMAP visualization of all candidates and jobs as points in embedding space;
  proximity on the map reflects semantic similarity between a CV and a job description

---

## Models

| Model               | Size   | Role                                      |
|---------------------|--------|-------------------------------------------|
| granite4.1:3b       | ~2GB   | CV parsing + recommendation generation    |
| embeddinggemma:300m | ~300MB | Semantic embedding for match scoring      |

Both run via Ollama locally. Never loaded simultaneously — Ollama swaps them as needed.