from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import router as v1_router
from app.core.config import get_settings
from app.core.error_handlers import domain_error_handler
from app.core.exceptions import ChatError, DocumentProcessingError
from app.core.logging import configure_logging
from app.rag.vector_store.faiss_store import get_vector_store
from app.services.document_registry_service import get_document_registry

configure_logging()

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Carga el índice FAISS y el registro de documentos existentes al iniciar la aplicación."""
    get_vector_store()
    get_document_registry()
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(DocumentProcessingError, domain_error_handler)
app.add_exception_handler(ChatError, domain_error_handler)

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
