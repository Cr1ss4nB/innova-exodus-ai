import logging
from pathlib import Path

from app.core.config import get_settings
from app.core.exceptions import DocumentProcessingError, EmbeddingGenerationError
from app.models.document import ProcessingResult
from app.rag.embeddings.gemini_embeddings import get_embeddings_model
from app.rag.loaders.pdf_loader import extract_text_from_pdf
from app.rag.splitters.text_splitter import split_pages_into_chunks
from app.rag.vector_store.faiss_store import get_vector_store

logger = logging.getLogger(__name__)


def process_document(file_path: Path, original_filename: str, document_id: str) -> ProcessingResult:
    """Extrae, divide, genera embeddings e indexa un PDF en el vector store."""
    settings = get_settings()

    logger.info("Procesando documento '%s' (document_id=%s)", original_filename, document_id)

    pages = extract_text_from_pdf(file_path)
    chunks = split_pages_into_chunks(
        document_id=document_id,
        filename=original_filename,
        pages=pages,
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )

    if not chunks:
        raise DocumentProcessingError(f"No se generaron fragmentos para el documento: {original_filename}")

    embeddings_model = get_embeddings_model()
    try:
        vectors = embeddings_model.embed_documents([chunk.text for chunk in chunks])
    except Exception as error:
        raise EmbeddingGenerationError(f"Fallo al generar embeddings para: {original_filename}") from error

    vector_store = get_vector_store()
    vector_store.add_chunks(chunks, vectors)

    logger.info(
        "Documento '%s' procesado: %d páginas, %d fragmentos indexados",
        original_filename,
        len(pages),
        len(chunks),
    )

    return ProcessingResult(
        document_id=document_id,
        filename=original_filename,
        total_pages=len(pages),
        total_chunks=len(chunks),
    )
