import logging
import uuid
from datetime import datetime, timezone

from app.core.config import get_settings
from app.core.exceptions import DuplicateDocumentError
from app.models.document import DocumentRecord
from app.rag.vector_store.faiss_store import get_vector_store
from app.services.document_processing_service import process_document
from app.services.document_registry_service import get_document_registry
from app.utils.file_hashing import compute_sha256
from app.utils.file_storage import delete_file, save_file_bytes
from app.utils.file_validation import validate_pdf_upload

logger = logging.getLogger(__name__)


def upload_document(filename: str, content_type: str | None, content: bytes) -> DocumentRecord:
    """Valida, guarda, procesa e indexa un PDF subido, y lo registra en el sistema."""
    settings = get_settings()

    validate_pdf_upload(
        filename=filename,
        content_type=content_type,
        file_size=len(content),
        max_size_mb=settings.max_upload_size_mb,
    )

    file_hash = compute_sha256(content)
    registry = get_document_registry()

    existing = registry.find_by_hash(file_hash)
    if existing is not None:
        raise DuplicateDocumentError(
            f"Este documento ya fue registrado como '{existing.filename}' (id={existing.document_id})"
        )

    document_id = str(uuid.uuid4())
    stored_filename = f"{document_id}.pdf"
    file_path = settings.uploads_path / stored_filename

    save_file_bytes(file_path, content)

    try:
        result = process_document(file_path, filename, document_id)
    except Exception:
        delete_file(file_path)
        raise

    record = DocumentRecord(
        document_id=document_id,
        filename=filename,
        stored_filename=stored_filename,
        upload_date=datetime.now(timezone.utc),
        total_pages=result.total_pages,
        total_chunks=result.total_chunks,
        size_bytes=len(content),
        file_hash=file_hash,
    )

    registry.add(record)
    logger.info("Documento registrado y disponible para consulta: %s (%s)", filename, document_id)

    return record


def list_documents() -> list[DocumentRecord]:
    """Retorna todos los documentos registrados."""
    return get_document_registry().list_all()


def delete_document(document_id: str) -> tuple[DocumentRecord, int]:
    """Elimina un documento: sus vectores en FAISS, su archivo físico y su registro."""
    registry = get_document_registry()
    record = registry.get(document_id)

    vectors_removed = get_vector_store().remove_by_document_id(document_id)

    file_path = get_settings().uploads_path / record.stored_filename
    delete_file(file_path)

    registry.remove(document_id)

    logger.info(
        "Documento eliminado: %s (%s), %d vectores removidos",
        record.filename,
        document_id,
        vectors_removed,
    )

    return record, vectors_removed
