import logging

from app.models.chat import ChatAnswer, ChatSource
from app.rag.chain import answer_question

logger = logging.getLogger(__name__)


def ask(question: str) -> ChatAnswer:
    """Ejecuta el flujo RAG completo y arma la respuesta con sus fuentes, sin duplicados."""
    answer, chunks = answer_question(question)

    seen: set[tuple[str, int]] = set()
    sources: list[ChatSource] = []

    for chunk in chunks:
        key = (chunk.filename, chunk.page_number)
        if key in seen:
            continue
        seen.add(key)
        sources.append(ChatSource(document=chunk.filename, page=chunk.page_number))

    logger.info("Respuesta generada con %d fuente(s) citada(s)", len(sources))

    return ChatAnswer(answer=answer, sources=sources)
