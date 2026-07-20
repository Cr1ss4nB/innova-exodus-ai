from app.models.document import PageContent
from app.rag.splitters.text_splitter import split_pages_into_chunks


def test_splits_text_and_preserves_page_number():
    pages = [
        PageContent(page_number=1, text="a" * 50),
        PageContent(page_number=2, text="b" * 50),
    ]

    chunks = split_pages_into_chunks(
        document_id="doc-1",
        filename="ejemplo.pdf",
        pages=pages,
        chunk_size=20,
        chunk_overlap=0,
    )

    assert len(chunks) > 0
    assert all(chunk.document_id == "doc-1" for chunk in chunks)
    assert {chunk.page_number for chunk in chunks} == {1, 2}


def test_ignores_empty_pages():
    pages = [PageContent(page_number=1, text="")]

    chunks = split_pages_into_chunks(
        document_id="doc-2",
        filename="vacio.pdf",
        pages=pages,
        chunk_size=100,
        chunk_overlap=0,
    )

    assert chunks == []
