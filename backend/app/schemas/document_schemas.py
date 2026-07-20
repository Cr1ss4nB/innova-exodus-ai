from datetime import datetime

from pydantic import BaseModel

from app.models.document import DocumentRecord


class DocumentResponse(BaseModel):
    """Representación de un documento registrado, expuesta por la API."""

    document_id: str
    filename: str
    upload_date: datetime
    total_pages: int
    total_chunks: int
    size_bytes: int

    @classmethod
    def from_record(cls, record: DocumentRecord) -> "DocumentResponse":
        return cls(
            document_id=record.document_id,
            filename=record.filename,
            upload_date=record.upload_date,
            total_pages=record.total_pages,
            total_chunks=record.total_chunks,
            size_bytes=record.size_bytes,
        )


class DocumentListResponse(BaseModel):
    """Listado de documentos registrados."""

    documents: list[DocumentResponse]
    total: int


class DocumentDeleteResponse(BaseModel):
    """Confirmación de eliminación de un documento."""

    document_id: str
    filename: str
    vectors_removed: int
    message: str
