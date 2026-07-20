import logging

from app.models.chat import ChatAnswer, ChatSource
from app.prompts.greeting_prompt import GREETING_RESPONSE
from app.prompts.system_prompt import INSUFFICIENT_INFO_MARKER
from app.rag.chain import answer_question
from app.rag.intent import is_greeting

logger = logging.getLogger(__name__)


def ask(question: str) -> ChatAnswer:
    """Ejecuta el flujo de chat: responde saludos directamente o ejecuta el flujo RAG completo."""
    if is_greeting(question):
        logger.info("Mensaje detectado como saludo o cortesía, se responde sin consultar FAISS")
        return ChatAnswer(answer=GREETING_RESPONSE, sources=[])

    answer, chunks = answer_question(question)

    if INSUFFICIENT_INFO_MARKER.lower() in answer.lower():
        logger.info("El modelo indicó que no hay información suficiente, se omiten las fuentes")
        return ChatAnswer(answer=answer, sources=[])

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
