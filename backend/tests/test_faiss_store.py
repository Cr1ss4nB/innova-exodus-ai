import pytest

from app.models.document import DocumentChunk
from app.rag.vector_store.faiss_store import FaissVectorStore


@pytest.fixture
def store(tmp_path):
    return FaissVectorStore(index_dir=tmp_path / "vector_store", dimension=4)


def _chunk(document_id, index):
    return DocumentChunk(
        document_id=document_id,
        filename=f"{document_id}.pdf",
        page_number=1,
        chunk_index=index,
        text=f"fragmento {index}",
    )


def test_removes_all_vectors_when_last_document_is_deleted(store):
    chunks = [_chunk("doc-1", 0), _chunk("doc-1", 1)]
    embeddings = [[0.1, 0.2, 0.3, 0.4], [0.5, 0.6, 0.7, 0.8]]

    store.add_chunks(chunks, embeddings)
    assert store.total_vectors == 2

    removed = store.remove_by_document_id("doc-1")

    assert removed == 2
    assert store.total_vectors == 0


def test_removing_one_document_keeps_the_others(store):
    store.add_chunks([_chunk("doc-1", 0)], [[0.1, 0.1, 0.1, 0.1]])
    store.add_chunks([_chunk("doc-2", 0)], [[0.9, 0.9, 0.9, 0.9]])

    removed = store.remove_by_document_id("doc-1")

    assert removed == 1
    assert store.total_vectors == 1


def test_removing_unknown_document_id_removes_nothing(store):
    store.add_chunks([_chunk("doc-1", 0)], [[0.1, 0.1, 0.1, 0.1]])

    removed = store.remove_by_document_id("id-inexistente")

    assert removed == 0
    assert store.total_vectors == 1
