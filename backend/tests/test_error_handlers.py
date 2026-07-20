from fastapi import status

from app.core.error_handlers import _resolve_status_code
from app.core.exceptions import (
    DocumentNotFoundError,
    DuplicateDocumentError,
    EmbeddingGenerationError,
    InvalidUploadError,
    LLMGenerationError,
)


def test_maps_known_exceptions_to_expected_status_codes():
    assert _resolve_status_code(InvalidUploadError("x")) == status.HTTP_400_BAD_REQUEST
    assert _resolve_status_code(DuplicateDocumentError("x")) == status.HTTP_409_CONFLICT
    assert _resolve_status_code(DocumentNotFoundError("x")) == status.HTTP_404_NOT_FOUND
    assert _resolve_status_code(EmbeddingGenerationError("x")) == status.HTTP_502_BAD_GATEWAY
    assert _resolve_status_code(LLMGenerationError("x")) == status.HTTP_502_BAD_GATEWAY


def test_unknown_exception_maps_to_internal_error():
    assert _resolve_status_code(ValueError("x")) == status.HTTP_500_INTERNAL_SERVER_ERROR
