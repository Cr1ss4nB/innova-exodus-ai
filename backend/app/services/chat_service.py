import logging

from app.models.chat import ChatAnswer, ChatSource
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


def ask(question: str) -> ChatAnswer:
    """Ejecuta el flujo de chat: solo las preguntas reales consultan FAISS y Gemini.

    Saludos, agradecimientos y despedidas se responden con reglas simples, sin tocar el
    índice ni el modelo de lenguaje. Cualquier otro mensaje se trata como una pregunta real
    y sigue el pipeline RAG completo (embedding de la pregunta, búsqueda en FAISS, construcción
    del prompt y generación con Gemini), exactamente igual que antes.
    """
    intent = classify_intent(question)

    if intent in _CANNED_RESPONSES:
        logger.info("Mensaje clasificado como '%s', se responde sin consultar FAISS ni Gemini", intent)
        return ChatAnswer(answer=_CANNED_RESPONSES[intent], sources=[])

    if get_vector_store().total_vectors == 0:
        logger.info("No hay documentos indexados en FAISS, se responde sin consultar al modelo")
        return ChatAnswer(answer=INSUFFICIENT_INFO_RESPONSE, sources=[])

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
