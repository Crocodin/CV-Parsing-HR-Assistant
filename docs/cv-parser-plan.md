# CV Parser & HR Assistant — Project Plan

## Folder Structure

```
CV-Parsing-HR-Assistant
├─ .dockerignore
├─ backend/
│  ├─ alembic.ini
│  ├─ app/
│  │  ├─ api/                   <-- API endpoints for FastAPI
│  │  │  ├─ candidates.py
│  │  │  ├─ jobs.py
│  │  │  ├─ points_2d.py
│  │  │  └─ scores.py
│  │  ├─ config/
│  │  │  └─ config.py           <-- FastAPI configuration, only for native development, not for Docker
│  │  ├─ db/
│  │  │  ├─ migrations          <-- Alembic migrations folder
│  │  │  │  └─ versions/
│  │  │  ├─ session.py
│  │  │  └─ tables.sql
│  │  ├─ main.py
│  │  ├─ models/                <-- SQLAlchemy models for database tables
│  │  ├─ repositories/
│  │  ├─ services/
│  │  │  ├─ embeddings.py       <-- Embedding generation
│  │  │  ├─ extractor.py
│  │  │  ├─ merger.py
│  │  │  ├─ ollama.py           <-- Ollama API calls for parsing
│  │  │  ├─ ollama_prompts.py   <-- Ollama prompt templates
│  │  │  ├─ recommender.py      <-- Recommendation generation
│  │  │  ├─ scorer.py    
│  │  │  ├─ splitter.py
│  │  │  └─ umap_points.py      <-- UMAP calls for dimensionality reduction
│  │  └─ workers/
│  ├─ Dockerfile
│  ├─ requirements.txt
├─ docker-compose.yml
├─ docs/
│  ├─ cv-parser-architecture.md
│  ├─ cv-parser-plan.md         <-- YOU ARE HERE
│  └─ how-to-code.md
├─ frontend/
│  ├─ electron/
│  │  ├─ main.ts
│  │  └─ preload.ts
│  ├─ index.html
│  ├─ src/
│  │  ├─ api/                   <-- API calls to FastAPI backend>
│  │  │  ├─ Api.tsx
│  │  │  ├─ CandidateAPI.tsx
│  │  │  ├─ EmbeddingAPI.tsx
│  │  │  └─ JobAPI.tsx
│  │  ├─ App.scss
│  │  ├─ App.tsx
│  │  ├─ components/
│  │  │  ├─ CandidateView.scss
│  │  │  ├─ CandidateView.tsx
│  │  │  ├─ EmbeddingCanvas.scss
│  │  │  ├─ EmbeddingCanvas.tsx
│  │  │  ├─ JobView.scss
│  │  │  ├─ JobView.tsx
│  │  │  ├─ ViewEmbeddings.scss
│  │  │  └─ ViewEmbeddings.tsx
│  │  ├─ index.scss
│  │  ├─ main.tsx
│  │  ├─ model
│  │  │  ├─ CV.tsx
│  │  │  ├─ CVPoint2D.tsx
│  │  │  ├─ Job.tsx
│  │  │  ├─ JobPoint2D.tsx
│  │  │  └─ Task.tsx
│  │  ├─ types
│  │  │  └─ electron.d.ts
│  │  └─ utils
│  │     └─ saveCV.tsx
└─ send_files.sh

```

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

Phase 4 - Frontend
```
