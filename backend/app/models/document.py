from dataclasses import dataclass
from datetime import datetime


@dataclass
class PageContent:
    """Texto extraído de una página específica de un PDF."""

    page_number: int
    text: str


@dataclass
class DocumentChunk:
    """Fragmento de texto listo para generar su embedding e indexarlo."""

    document_id: str
    filename: str
    page_number: int
    chunk_index: int
    text: str


@dataclass
class ProcessingResult:
    """Resultado del procesamiento completo de un documento."""

    document_id: str
    filename: str
    total_pages: int
    total_chunks: int


@dataclass
class DocumentRecord:
    """Registro persistente de un documento gestionado por el sistema."""

    document_id: str
    filename: str
    stored_filename: str
    upload_date: datetime
    total_pages: int
    total_chunks: int
    size_bytes: int
