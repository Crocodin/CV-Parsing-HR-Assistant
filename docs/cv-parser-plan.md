# CV Parser & HR Assistant — Project Plan

## Folder Structure

```
cv-parser/
│
├── docker-compose.yml
│
├── backend/                        
│   ├── `.venv`                     <- YOU NEED TO CREATE THE VENV, DO NOT COMMIT IT
│   ├── Dockerfile                  <- recipe for the FastAPI container
│   ├── requirements.txt
│   ├── `.env`                      <- YOU NEED TO CREATE THIS FILE, DO NOT COMMIT IT
│   └── app/
│       ├── main.py                 <- FastAPI app entry point
│       ├── config.py               <- env
│       │
│       ├── api/     
│       │   ├── jobs.py             <- upload/manage job postings
│       │   ├── candidates.py       <- upload CVs, view parsed results
│       │   └── scores.py           <- match scores, recommendations
│       │
│       ├── services/ 
│       │   ├── extractor.py        <- pdfplumber + python-docx
│       │   ├── splitter.py         <- section splitter (regex)
│       │   ├── ollama.py           <- qwen3.5:4b calls
│       │   ├── embeddings.py       <- nomic-embed-text
│       │   └── scorer.py
│       │
│       ├── models/                 
│       │
│       ├── workers/
│       │   └── tasks.py            <- Celery + Redis
│       │
│       └── db/    
│           ├── `password.txt`      <- YOU NEED TO CREATE THIS FILE WITH THE DB PASSWORD, DO NOT COMMIT IT
│           ├── session.py          <- PostgreSQL connection
│           └── migrations/         <- Alembic migration files
│
├── frontend/                       
│   └── (Flutter project)
│       ├── lib/
│       │   ├── main.dart
│       │   ├── screens/
│       │   │   ├── dashboard_screen.dart
│       │   │   ├── upload_screen.dart
│       │   │   └── candidate_screen.dart
│       │   ├── widgets/
│       │   └── services/
│       │       └── api_service.dart 
│       └── pubspec.yaml
│
└── docs/
    ├── cv-parser-architecture.md
    └── cv-parser-plan.md            <- this file
```

---

## Build Order

```
Phase 1 — Foundation
├── Docker Compose + Dockerfile
├── FastAPI skeleton (main.py, config, folder structure)
└── PostgreSQL connection (db/session.py)

Phase 2 — Core Pipeline
├── extractor.py -> splitter.py -> ollama.py
├── Celery + Redis queue
└── database models → embeddings.py → scorer.py

Phase 3 — API Endpoints
├── POST /jobs              -> upload job description
├── POST /candidates        -> upload CV, trigger processing queue
├── GET  /candidates        -> list all candidates with scores
└── GET  /candidates/{id}   -> single candidate detail + recommendation

Frontend
├── Upload screen           -> calls POST /jobs and POST /candidates
├── Dashboard screen        -> calls GET /candidates
└── Candidate screen        -> calls GET /candidates/{id}
```

## Key Reminders

- **Ollama runs natively** — not in Docker. Has direct GPU access. FastAPI reaches it at `host.docker.internal:11434`
- **Flutter runs natively** — not in Docker. Talks to FastAPI at `localhost:8000`
- **Only FastAPI + PostgreSQL + Redis** run inside Docker
- **Never recompute** — if a score or recommendation is already in the database, return it from there
- **LLM only for top candidates** — embeddings score everyone, qwen3.5:4b only explains candidates above the match threshold