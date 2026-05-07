# CV Parser & HR Assistant — Architecture Overview

## Project Summary

An AI-powered desktop application that helps HR personnel screen CVs faster and with less bias.
It parses CVs, extracts structured data, compares candidates against job descriptions, generates  
match scores, and provides explainable recommendations. The system supports human decision-making, it does not automate hiring decisions.

Team size: 3 students.

---

## Full Tech Stack

| Layer                           | Technology                           | Optional |
|---------------------------------|--------------------------------------|----------|
| Desktop Frontend                | Flutter (Dart)                       | No.      |
| Backend API                     | FastAPI (Python)                     | No.      |
| Database                        | PostgreSQL                           | No.      |
| Migrations                      | Alembic                              | Yes      |
| Job Queue                       | Redis + Celery                       | Yes      |
| LLM (parsing + recommendations) | Ollama — qwen3.5:4b                  | No.      |
| Embeddings (scoring)            | Ollama — nomic-embed-text-v2-moe     | No.      |
| PDF extraction                  | pdfplumber                           | No.      |
| DOCX extraction                 | python-docx                          | No.      |
| Auth                            | JWT                                  | Yes      |
| Containerization                | Docker Compose (partial — see below) | No.      |

---

## What Runs Where

```
Your Machine (native)
├── Ollama                  -> serves qwen3.5:4b and nomic-embed-text-v2-moe
│     └── accessible at localhost:11434
└── Flutter desktop app     -> talks to FastAPI via HTTP

Docker Compose
├── FastAPI                 -> talks to Ollama at host.docker.internal:11434
└── PostgreSQL              -> data persistence via Docker volume
```

Flutter and Ollama run natively on the machine. FastAPI and PostgreSQL run inside Docker.
No GPU passthrough needed — Ollama has direct access to the GPU as a native process.

---

## CV Processing Pipeline

```
User uploads PDF or DOCX
        ↓
pdfplumber / python-docx        -> raw text extraction
        ↓
Custom section splitter         -> splits text into: header, education, experience, skills
(rule-based, regex, no LLM)
        ↓
Celery queue                    -> jobs processed one at a time, Ollama not hammered
        ↓ -> this layer of Celery is optional, we will se when developing if we have time to make this too
qwen3.5:4b via Ollama           -> one focused prompt per section → structured JSON per section
        ↓
Assemble final candidate JSON
{ name, email, skills[], experience[], education[] }
        ↓
PostgreSQL                      -> save candidate + parsed data
```

---

## Matching & Scoring Pipeline

```
Candidate JSON + Job Description JSON
        ↓
nomic-embed-text                -> convert both to embedding vectors
        ↓                       (the job description embendings will be cached)
Cosine similarity               -> match score 0–100%
        ↓
PostgreSQL                      -> save score
        ↓
If score > threshold (e.g. 50%)
        ↓
qwen3.5:4b via Ollama           -> generate explanation + recommendations
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
| recommendations | qwen3.5 explanation text per match           |

Rule: anything expensive to compute gets stored so it is never recomputed.

---

## Key Architectural Decisions

- **No external APIs** — everything runs locally, no costs, no internet dependency
- **Section-by-section LLM parsing** — smaller prompts = faster inference, more reliable JSON, easier debugging
- **Embeddings for scoring, LLM for explanation** — fast semantic matching first, expensive LLM call only when needed
- **Celery queue** — prevents Ollama from being hammered when multiple CVs are uploaded at once
- **Alembic** — database schema changes tracked like code, no manual SQL alterations

---

## What the HR Dashboard Shows (Flutter)

- Upload a job description
- Upload one or multiple CVs
- See a ranked list of candidates with match scores
- Click a candidate to see extracted skills, experience, education
- Read the AI-generated explanation and recommendations
- View metrics: total screened, average score, top candidates

---

## Models

| Model             | Size           | Role                                           |
|-------------------|----------------|------------------------------------------------|
| qwen3.5:4b        | 3.4GB (Q4_K_M) | CV section parsing + recommendation generation |
| nomic-embed-text  | 274MB          | Semantic embedding for match scoring           |

Both run via Ollama locally. Total ~3.7GB — within 4GB VRAM since they are never
loaded simultaneously. Ollama swaps them as needed.