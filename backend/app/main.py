from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import router as v1_router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.rag.vector_store.faiss_store import get_vector_store

configure_logging()

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Carga el índice FAISS existente (si lo hay) al iniciar la aplicación."""
    get_vector_store()
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router)


@app.get("/")
def read_root() -> dict:
    """Información básica de la API."""
    return {
        "application": "Innova Exodus",
        "version": "v1",
        "status": "running",
        "documentation": "/docs",
        "health": "/api/v1/health",
    }
