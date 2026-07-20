from dataclasses import dataclass


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
