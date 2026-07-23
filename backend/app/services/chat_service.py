import logging

from app.models.chat import ChatAnswer, ChatSource, ChatTurn
from app.prompts.farewell_prompt import GOODBYE_RESPONSE, GRATITUDE_RESPONSE
from app.prompts.greeting_prompt import GREETING_RESPONSE
from app.prompts.system_prompt import INSUFFICIENT_INFO_MARKER, INSUFFICIENT_INFO_RESPONSE
from app.rag.chain import answer_question
from app.rag.intent import classify_intent
from app.rag.vector_store.faiss_store import get_vector_store

logger = logging.getLogger(__name__)

_CANNED_RESPONSES = {
    "greeting": GREETING_RESPONSE,
    "gratitude": GRATITUDE_RESPONSE,
    "goodbye": GOODBYE_RESPONSE,
}


def ask(question: str, history: list[ChatTurn] | None = None) -> ChatAnswer:
    """Ejecuta el flujo de chat: solo las preguntas reales consultan FAISS y Gemini.

    El historial es efímero y lo aporta el frontend en cada solicitud; el backend nunca lo
    almacena. Se usa únicamente para ayudar a interpretar preguntas de seguimiento, sin alterar
    el pipeline RAG de fondo (mismo índice, mismo modelo, una sola llamada a Gemini por consulta).
    """
    history = history or []
    intent = classify_intent(question)

    if intent in _CANNED_RESPONSES:
        logger.info("Mensaje clasificado como '%s', se responde sin consultar FAISS ni Gemini", intent)
        return ChatAnswer(answer=_CANNED_RESPONSES[intent], sources=[])

    if get_vector_store().total_vectors == 0:
        logger.info("No hay documentos indexados en FAISS, se responde sin consultar al modelo")
        return ChatAnswer(answer=INSUFFICIENT_INFO_RESPONSE, sources=[])

    answer, chunks = answer_question(question, history)

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
