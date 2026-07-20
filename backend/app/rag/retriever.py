import logging

from app.core.config import get_settings
from app.core.exceptions import EmbeddingGenerationError
from app.models.document import RetrievedChunk
from app.rag.embeddings.gemini_embeddings import get_embeddings_model
from app.rag.vector_store.faiss_store import get_vector_store

logger = logging.getLogger(__name__)


def retrieve_relevant_chunks(question: str) -> list[RetrievedChunk]:
    """Recupera los fragmentos más relevantes para una pregunta, usando embeddings y búsqueda en FAISS."""
    settings = get_settings()
    embeddings_model = get_embeddings_model()

    try:
        query_vector = embeddings_model.embed_query(question)
    except Exception as error:
        raise EmbeddingGenerationError("Fallo al generar el embedding de la pregunta") from error

    results = get_vector_store().similarity_search(query_vector, top_k=settings.top_k)

    logger.info("Recuperados %d fragmentos relevantes para la consulta", len(results))

    return [
        RetrievedChunk(
            document_id=result["document_id"],
            filename=result["filename"],
            page_number=result["page_number"],
            text=result["text"],
            distance=result["distance"],
        )
        for result in results
    ]
