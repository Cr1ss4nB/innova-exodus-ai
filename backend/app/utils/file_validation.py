from app.core.exceptions import InvalidUploadError

ALLOWED_CONTENT_TYPE = "application/pdf"
ALLOWED_EXTENSION = ".pdf"


def validate_pdf_upload(filename: str, content_type: str | None, file_size: int, max_size_mb: int) -> None:
    """Valida que el archivo subido sea un PDF y no exceda el tamaño máximo permitido."""
    if not filename.lower().endswith(ALLOWED_EXTENSION):
        raise InvalidUploadError(f"Solo se permiten archivos PDF: {filename}")

    if content_type is not None and content_type != ALLOWED_CONTENT_TYPE:
        raise InvalidUploadError(f"Tipo de contenido no soportado: {content_type}")

    if file_size == 0:
        raise InvalidUploadError(f"El archivo está vacío: {filename}")

    max_size_bytes = max_size_mb * 1024 * 1024
    if file_size > max_size_bytes:
        raise InvalidUploadError(f"El archivo excede el tamaño máximo permitido de {max_size_mb}MB")
