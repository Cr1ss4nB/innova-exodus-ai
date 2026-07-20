from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.models.document import DocumentChunk, PageContent


def split_pages_into_chunks(
    document_id: str,
    filename: str,
    pages: list[PageContent],
    chunk_size: int,
    chunk_overlap: int,
) -> list[DocumentChunk]:
    """Divide el texto de cada página en fragmentos, conservando el número de página."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    chunks: list[DocumentChunk] = []
    chunk_index = 0

    for page in pages:
        if not page.text:
            continue

        for fragment in splitter.split_text(page.text):
            chunks.append(
                DocumentChunk(
                    document_id=document_id,
                    filename=filename,
                    page_number=page.page_number,
                    chunk_index=chunk_index,
                    text=fragment,
                )
            )
            chunk_index += 1

    return chunks
