from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from app.api.candidates import route as candidate_route
from app.api.jobs import router as jobs_router
from app.api.scores import router as scores_router
from app.api.points_2d import router as umap_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Perform any startup tasks here
    print("Starting up the CV Parsing HR Assistant API...")
    yield
    # Perform any shutdown tasks here
    print("Shutting down the CV Parsing HR Assistant API...")

app = FastAPI(
    title="CV Parsing HR Assistant API",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

app.include_router(candidate_route, prefix="/candidate", tags=["candidate"])
app.include_router(jobs_router, prefix="/jobs", tags=["jobs"])
app.include_router(scores_router, prefix="/scores", tags=["scores"])
app.include_router(umap_router, prefix="/umap", tags=["umap"])