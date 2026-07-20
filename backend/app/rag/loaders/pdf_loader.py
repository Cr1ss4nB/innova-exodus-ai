from pathlib import Path

import fitz

from app.core.exceptions import EmptyPDFError, InvalidPDFError
from app.models.document import PageContent


def extract_text_from_pdf(file_path: Path) -> list[PageContent]:
    """Abre un PDF, extrae el texto de cada página y valida que sea legible."""
    try:
        document = fitz.open(str(file_path))
    except Exception as error:
        raise InvalidPDFError(f"No se pudo abrir el archivo PDF: {file_path.name}") from error

    try:
        pages = [
            PageContent(page_number=index + 1, text=page.get_text().strip())
            for index, page in enumerate(document)
        ]
    finally:
        document.close()

    if not any(page.text for page in pages):
        raise EmptyPDFError(f"El PDF no contiene texto extraíble: {file_path.name}")

    return pages
