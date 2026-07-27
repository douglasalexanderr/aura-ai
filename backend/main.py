from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api import router as api_router
from app.db import init_db

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"
MEDIA_DIR = BASE_DIR / "data" / "media"

app = FastAPI(
    title="AURA AI",
    version="0.3.0",
    description="Marketing autónomo, CRM y generación de campañas",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

MEDIA_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/assets", StaticFiles(directory=FRONTEND_DIR), name="assets")
app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")
app.include_router(api_router, prefix="/api")


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "AURA AI", "version": "0.3.0"}


@app.get("/")
def web_app():
    return FileResponse(FRONTEND_DIR / "index.html")
