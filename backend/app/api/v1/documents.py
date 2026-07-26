from fastapi import APIRouter, File, UploadFile, status
from fastapi.responses import FileResponse

from app.schemas.document_schemas import (
    CorporateDocumentsLoadResponse,
    DocumentDeleteResponse,
    DocumentListResponse,
    DocumentResponse,
)
from app.services.document_service import (
    delete_document,
    get_document_file_path,
    list_documents,
    load_corporate_documents,
    upload_document,
)

router = APIRouter(prefix="/documents")


@router.post("", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document_endpoint(file: UploadFile = File(...)) -> DocumentResponse:
    """Sube un PDF, lo procesa y lo indexa en el vector store."""
    content = await file.read()
    record = upload_document(
        filename=file.filename or "documento.pdf",
        content_type=file.content_type,
        content=content,
    )
    return DocumentResponse.from_record(record)


@router.post("/corporate", response_model=CorporateDocumentsLoadResponse)
def load_corporate_documents_endpoint() -> CorporateDocumentsLoadResponse:
    """Procesa e indexa los PDFs de resources/documents/, omitiendo automáticamente
    (sin error) los que ya estén registrados según su hash SHA-256."""
    loaded, already_existing = load_corporate_documents()
    return CorporateDocumentsLoadResponse(
        loaded=[DocumentResponse.from_record(record) for record in loaded],
        already_existing=already_existing,
        total_loaded=len(loaded),
        total_already_existing=len(already_existing),
    )


@router.get("", response_model=DocumentListResponse)
def list_documents_endpoint() -> DocumentListResponse:
    """Lista todos los documentos registrados en el sistema."""
    records = list_documents()
    return DocumentListResponse(
        documents=[DocumentResponse.from_record(record) for record in records],
        total=len(records),
    )


@router.get("/{document_id}/view")
def view_document_endpoint(document_id: str) -> FileResponse:
    """Sirve el PDF original para visualizarlo en el navegador, sin forzar su descarga."""
    file_path, filename = get_document_file_path(document_id)
    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        headers={"Content-Disposition": f'inline; filename="{filename}"'},
    )


@router.delete("/{document_id}", response_model=DocumentDeleteResponse)
def delete_document_endpoint(document_id: str) -> DocumentDeleteResponse:
    """Elimina un documento, su archivo físico y sus vectores asociados en FAISS."""
    record, vectors_removed = delete_document(document_id)
    return DocumentDeleteResponse(
        document_id=record.document_id,
        filename=record.filename,
        vectors_removed=vectors_removed,
        message="Documento eliminado correctamente",
    )
