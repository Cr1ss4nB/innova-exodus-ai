import logging
from functools import lru_cache

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import get_settings
from app.core.exceptions import LLMGenerationError
from app.models.chat import ChatTurn
from app.models.document import RetrievedChunk
from app.prompts.system_prompt import SYSTEM_PROMPT_TEMPLATE
from app.rag.retriever import retrieve_relevant_chunks

logger = logging.getLogger(__name__)


@lru_cache
def get_chat_model() -> ChatGoogleGenerativeAI:
    """Retorna el modelo de chat de Gemini, configurado según el .env."""
    settings = get_settings()
    return ChatGoogleGenerativeAI(
        model=settings.model_name,
        google_api_key=settings.gemini_api_key,
        temperature=settings.temperature,
    )


def _build_context(chunks: list[RetrievedChunk]) -> str:
    """Combina los fragmentos recuperados en un único bloque de contexto, citando su fuente."""
    if not chunks:
        return "No se encontró información relevante en la base documental."

    blocks = [f"[Fuente: {chunk.filename}, página {chunk.page_number}]\n{chunk.text}" for chunk in chunks]
    return "\n\n".join(blocks)


def _build_retrieval_query(question: str, history: list[ChatTurn]) -> str:
    """Enriquece el texto usado para la búsqueda semántica con las preguntas previas de la
    conversación, para mejorar la recuperación en preguntas de seguimiento (por ejemplo,
    "¿y qué más?"). No altera la pregunta que se le muestra al modelo, solo el texto usado
    para buscar en FAISS. La transformación es siempre la misma, sin detectar frases concretas."""
    if not history:
        return question

    previous_questions = " ".join(turn.question for turn in history)
    return f"{previous_questions} {question}"


def _build_history_messages(history: list[ChatTurn]) -> list:
    """Convierte el historial efímero en mensajes de LangChain para insertarlos en el prompt."""
    messages: list = []
    for turn in history:
        messages.append(HumanMessage(content=turn.question))
        messages.append(AIMessage(content=turn.answer))
    return messages


def answer_question(
    question: str, history: list[ChatTurn] | None = None
) -> tuple[str, list[RetrievedChunk]]:
    """Ejecuta el flujo RAG completo: recupera contexto, construye el prompt y consulta a Gemini.

    El historial es opcional y efímero (aportado por el frontend en cada solicitud, nunca
    almacenado aquí). Se usa para mejorar la recuperación semántica y para que el modelo
    interprete preguntas de seguimiento, pero sigue habiendo una única llamada a Gemini por
    consulta, igual que sin historial.
    """
    history = history or []

    retrieval_query = _build_retrieval_query(question, history)
    chunks = retrieve_relevant_chunks(retrieval_query)
    context = _build_context(chunks)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT_TEMPLATE),
            MessagesPlaceholder("history", optional=True),
            ("human", "{question}"),
        ]
    )
    chain = prompt | get_chat_model() | StrOutputParser()

    logger.info(
        "Consultando a Gemini para la pregunta: '%s' (con %d turno(s) de historial)",
        question,
        len(history),
    )

    try:
        answer = chain.invoke(
            {
                "context": context,
                "question": question,
                "history": _build_history_messages(history),
            }
        )
    except Exception as error:
        raise LLMGenerationError("Fallo al generar la respuesta con el modelo de lenguaje") from error

    return answer, chunks
