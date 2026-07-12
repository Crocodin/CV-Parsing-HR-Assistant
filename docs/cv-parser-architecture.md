# CV Parser & HR Assistant — Architecture Overview

## Project Summary

An AI-powered desktop application that helps HR personnel screen CVs faster and with less bias.
It parses CVs, extracts structured data, compares candidates against job descriptions, generates  
match scores, and provides explainable recommendations. The system supports human decision-making, it does not automate hiring decisions.

---

## Full Tech Stack

| Layer                           | Technology                           | 
|---------------------------------|--------------------------------------|
| Desktop Frontend                | React (Electron)                     |
| Backend API                     | FastAPI (Python)                     | 
| Database                        | PostgreSQL                           |
| Migrations                      | Alembic                              | 
| Job Queue                       | Celery                               | 
| LLM (parsing + recommendations) | Ollama — granite:4.1                 | 
| Embeddings (scoring)            | Ollama — embeddinggemma              | 
| PDF extraction                  | pdfplumber                           | 
| DOCX extraction                 | python-docx                          | 
| Containerization                | Docker Compose                       |

---

## What Runs Where

```
Native
├── Ollama                  
│     └── accessible at localhost:11434
└── React desktop app     -> talks to FastAPI via HTTP

Docker Compose
├── FastAPI                 
└── PostgreSQL              
```

## CV Processing Pipeline

```
User uploads PDF or DOCX
        ↓
pdfplumber / python-docx        -> raw text extraction
        ↓
Celery queue                    
        ↓
Granite:4.1 via Ollama          -> parse CV into structured JSON per section
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
embeddinggemma                 -> convert both to embedding vectors
        ↓                       (the job description embendings will be cached)
Cosine similarity               -> match score 0–100%
        ↓
PostgreSQL                      -> save score
        ↓
Granite:4.1 via Ollama           -> generate explanation + recommendations
"Candidate matches 78% — strong Python skills, missing Docker.
 Suggested interview question: ..."
        ↓
PostgreSQL                      -> save recommendation text
```

## What Gets Stored in PostgreSQL

| Table           | Purpose                                      |
|-----------------|----------------------------------------------|
| job_postings    | Job descriptions uploaded by HR              |
| candidates      | Parsed CV data (structured JSON)             |
| cv_embeddings   |                                              |
| match_scores    | Score between a candidate and a job posting  |
| recommendations | Granite:4.1 explanation text per match       |

Rule: anything expensive to compute gets stored so it is never recomputed.

---

## Key Architectural Decisions

- **No external APIs** — everything runs locally, no costs, no internet dependency
- **Embeddings for scoring, LLM for explanation** — fast semantic matching first, expensive LLM call only when needed
- **Celery queue** — prevents Ollama from being hammered when multiple CVs are uploaded at once
- **Alembic** — database schema changes tracked like code, no manual SQL alterations

---

## What the HR Dashboard Shows

- Upload a job description
- Upload CVs
- Click a candidate to see extracted skills, experience, education
- Read the AI-generated explanation and recommendations
- View metrics: total screened, average score, top candidates
- Map of candidate based on embeddings (UMAP projection) to visualize clusters of similar candidates
