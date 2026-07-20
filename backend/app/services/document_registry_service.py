import json
import logging
from dataclasses import asdict
from datetime import datetime
from functools import lru_cache
from pathlib import Path

from app.core.config import get_settings
from app.core.exceptions import DocumentNotFoundError
from app.models.document import DocumentRecord
from app.utils.file_hashing import compute_sha256

logger = logging.getLogger(__name__)


class DocumentRegistry:
    """Registro persistente de documentos, almacenado como JSON en backend/data."""

    def __init__(self, registry_path: Path):
        self.registry_path = registry_path
        self._documents: dict[str, dict] = {}
        self._load()

    def _load(self) -> None:
        if not self.registry_path.exists():
            logger.info("No existe un registro de documentos previo, se inicia uno vacío")
            return

        payload = json.loads(self.registry_path.read_text(encoding="utf-8"))
        self._documents = payload.get("documents", {})
        logger.info("Registro de documentos cargado con %d documentos", len(self._documents))

        self._migrate_missing_hashes()

    def _migrate_missing_hashes(self) -> None:
        """Calcula el hash de los documentos registrados antes de que existiera esta validación."""
        settings = get_settings()
        migrated = 0

        for document_id, data in self._documents.items():
            if data.get("file_hash"):
                continue

            file_path = settings.uploads_path / data["stored_filename"]
            if not file_path.exists():
                logger.warning(
                    "No se pudo migrar el hash del documento %s: archivo no encontrado (%s)",
                    document_id,
                    file_path,
                )
                continue

            data["file_hash"] = compute_sha256(file_path.read_bytes())
            migrated += 1

        if migrated:
            logger.info("Migración automática: se calculó el hash de %d documento(s) existentes", migrated)
            self._save()

    def _save(self) -> None:
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"documents": self._documents}
        self.registry_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def add(self, record: DocumentRecord) -> None:
        """Registra un nuevo documento en el sistema."""
        data = asdict(record)
        data["upload_date"] = record.upload_date.isoformat()
        self._documents[record.document_id] = data
        self._save()

    def get(self, document_id: str) -> DocumentRecord:
        """Retorna un documento registrado por su id, o lanza DocumentNotFoundError."""
        data = self._documents.get(document_id)
        if data is None:
            raise DocumentNotFoundError(f"No existe un documento con id: {document_id}")
        return self._to_record(data)

    def find_by_hash(self, file_hash: str) -> DocumentRecord | None:
        """Retorna el documento registrado con el hash dado, o None si no existe."""
        for data in self._documents.values():
            if data.get("file_hash") == file_hash:
                return self._to_record(data)
        return None

    def list_all(self) -> list[DocumentRecord]:
        """Retorna todos los documentos registrados."""
        return [self._to_record(data) for data in self._documents.values()]

    def remove(self, document_id: str) -> DocumentRecord:
        """Elimina un documento del registro y retorna sus datos."""
        data = self._documents.pop(document_id, None)
        if data is None:
            raise DocumentNotFoundError(f"No existe un documento con id: {document_id}")
        self._save()
        return self._to_record(data)

    @staticmethod
    def _to_record(data: dict) -> DocumentRecord:
        return DocumentRecord(
            document_id=data["document_id"],
            filename=data["filename"],
            stored_filename=data["stored_filename"],
            upload_date=datetime.fromisoformat(data["upload_date"]),
            total_pages=data["total_pages"],
            total_chunks=data["total_chunks"],
            size_bytes=data["size_bytes"],
            file_hash=data.get("file_hash", ""),
        )


@lru_cache
def get_document_registry() -> DocumentRegistry:
    """Retorna la instancia del registro de documentos, cacheada por proceso."""
    settings = get_settings()
    return DocumentRegistry(registry_path=settings.documents_registry_path)
