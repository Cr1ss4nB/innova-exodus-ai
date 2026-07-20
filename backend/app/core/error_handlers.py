import logging

from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    ChatError,
    DocumentNotFoundError,
    DocumentProcessingError,
    DuplicateDocumentError,
    EmbeddingGenerationError,
    EmptyPDFError,
    InvalidPDFError,
    InvalidUploadError,
    LLMGenerationError,
    VectorStoreError,
)

logger = logging.getLogger(__name__)

_STATUS_CODE_BY_EXCEPTION: dict[type[Exception], int] = {
    InvalidUploadError: status.HTTP_400_BAD_REQUEST,
    InvalidPDFError: status.HTTP_400_BAD_REQUEST,
    EmptyPDFError: status.HTTP_400_BAD_REQUEST,
    DuplicateDocumentError: status.HTTP_409_CONFLICT,
    DocumentNotFoundError: status.HTTP_404_NOT_FOUND,
    EmbeddingGenerationError: status.HTTP_502_BAD_GATEWAY,
    VectorStoreError: status.HTTP_502_BAD_GATEWAY,
    LLMGenerationError: status.HTTP_502_BAD_GATEWAY,
}


def _resolve_status_code(exc: Exception) -> int:
    """Determina el código HTTP apropiado según el tipo específico de excepción de dominio."""
    for exception_type, status_code in _STATUS_CODE_BY_EXCEPTION.items():
        if isinstance(exc, exception_type):
            return status_code
    return status.HTTP_500_INTERNAL_SERVER_ERROR


async def domain_error_handler(request: Request, exc: DocumentProcessingError | ChatError) -> JSONResponse:
    """Traduce cualquier excepción de dominio en una respuesta HTTP consistente."""
    status_code = _resolve_status_code(exc)

    if status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        logger.error("Error interno no clasificado: %s", exc, exc_info=True)
    else:
        logger.warning("Error de dominio (%s): %s", exc.__class__.__name__, exc)

    return JSONResponse(
        status_code=status_code,
        content={"detail": str(exc), "error_type": exc.__class__.__name__},
    )
