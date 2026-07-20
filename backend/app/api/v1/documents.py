from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.core.exceptions import (
    DocumentNotFoundError,
    DocumentProcessingError,
    EmbeddingGenerationError,
    EmptyPDFError,
    InvalidPDFError,
    InvalidUploadError,
    VectorStoreError,
)
from app.schemas.document_schemas import DocumentDeleteResponse, DocumentListResponse, DocumentResponse
from app.services.document_service import delete_document, list_documents, upload_document

router = APIRouter(prefix="/documents")


@router.post("", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document_endpoint(file: UploadFile = File(...)) -> DocumentResponse:
    """Sube un PDF, lo procesa y lo indexa en el vector store."""
    content = await file.read()

    try:
        record = upload_document(
            filename=file.filename or "documento.pdf",
            content_type=file.content_type,
            content=content,
        )
    except InvalidUploadError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)) from error
    except (InvalidPDFError, EmptyPDFError) as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)) from error
    except (EmbeddingGenerationError, VectorStoreError) as error:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(error)) from error
    except DocumentProcessingError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)) from error

    return DocumentResponse.from_record(record)


@router.get("", response_model=DocumentListResponse)
def list_documents_endpoint() -> DocumentListResponse:
    """Lista todos los documentos registrados en el sistema."""
    records = list_documents()
    return DocumentListResponse(
        documents=[DocumentResponse.from_record(record) for record in records],
        total=len(records),
    )


@router.delete("/{document_id}", response_model=DocumentDeleteResponse)
def delete_document_endpoint(document_id: str) -> DocumentDeleteResponse:
    """Elimina un documento, su archivo físico y sus vectores asociados en FAISS."""
    try:
        record, vectors_removed = delete_document(document_id)
    except DocumentNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except VectorStoreError as error:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(error)) from error

    return DocumentDeleteResponse(
        document_id=record.document_id,
        filename=record.filename,
        vectors_removed=vectors_removed,
        message="Documento eliminado correctamente",
    )
