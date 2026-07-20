import json
import logging
from functools import lru_cache
from pathlib import Path

import faiss
import numpy as np

from app.core.config import get_settings
from app.core.exceptions import VectorStoreError
from app.models.document import DocumentChunk

logger = logging.getLogger(__name__)


class FaissVectorStore:
    """Índice FAISS con persistencia en disco y metadata asociada a cada vector."""

    def __init__(self, index_dir: Path, dimension: int):
        self.index_dir = index_dir
        self.dimension = dimension
        self.index_path = index_dir / "index.faiss"
        self.metadata_path = index_dir / "metadata.json"

        self._index = faiss.IndexIDMap2(faiss.IndexFlatL2(dimension))
        self._metadata: dict[int, dict] = {}
        self._next_id = 0

        self._load()

    def _load(self) -> None:
        if not (self.index_path.exists() and self.metadata_path.exists()):
            logger.info("No existe un índice FAISS previo, se inicia uno vacío")
            return

        try:
            self._index = faiss.read_index(str(self.index_path))
            payload = json.loads(self.metadata_path.read_text(encoding="utf-8"))
            self._metadata = {int(vector_id): data for vector_id, data in payload["chunks"].items()}
            self._next_id = payload["next_id"]
        except Exception as error:
            raise VectorStoreError("No se pudo cargar el índice FAISS existente") from error

        logger.info("Índice FAISS cargado con %d vectores", self._index.ntotal)

    def save(self) -> None:
        """Persiste el índice y su metadata en backend/data/vector_store."""
        self.index_dir.mkdir(parents=True, exist_ok=True)

        try:
            faiss.write_index(self._index, str(self.index_path))
            payload = {"next_id": self._next_id, "chunks": self._metadata}
            self.metadata_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception as error:
            raise VectorStoreError("No se pudo persistir el índice FAISS") from error

        logger.info("Índice FAISS persistido con %d vectores", self._index.ntotal)

    def add_chunks(self, chunks: list[DocumentChunk], embeddings: list[list[float]]) -> None:
        """Agrega los embeddings de una lista de chunks al índice y persiste el resultado."""
        if len(chunks) != len(embeddings):
            raise VectorStoreError("La cantidad de chunks y de embeddings no coincide")

        if not chunks:
            return

        vectors = np.array(embeddings, dtype="float32")
        ids = np.array([self._next_id + offset for offset in range(len(chunks))], dtype="int64")

        try:
            self._index.add_with_ids(vectors, ids)
        except Exception as error:
            raise VectorStoreError("No se pudieron agregar los vectores al índice FAISS") from error

        for vector_id, chunk in zip(ids.tolist(), chunks):
            self._metadata[vector_id] = {
                "document_id": chunk.document_id,
                "filename": chunk.filename,
                "page_number": chunk.page_number,
                "chunk_index": chunk.chunk_index,
                "text": chunk.text,
            }

        self._next_id += len(chunks)
        self.save()

    def remove_by_document_id(self, document_id: str) -> int:
        """Elimina del índice todos los vectores asociados a un documento y retorna cuántos se eliminaron."""
        ids_to_remove = [
            vector_id for vector_id, data in self._metadata.items() if data["document_id"] == document_id
        ]

        if not ids_to_remove:
            return 0

        try:
            self._index.remove_ids(np.array(ids_to_remove, dtype="int64"))
        except Exception as error:
            raise VectorStoreError(f"No se pudieron eliminar los vectores del documento {document_id}") from error

        for vector_id in ids_to_remove:
            del self._metadata[vector_id]

        self.save()
        return len(ids_to_remove)

    @property
    def total_vectors(self) -> int:
        return self._index.ntotal


@lru_cache
def get_vector_store() -> FaissVectorStore:
    """Retorna la instancia del vector store, cacheada por proceso."""
    settings = get_settings()
    return FaissVectorStore(index_dir=settings.vector_store_path, dimension=settings.embedding_dimension)
