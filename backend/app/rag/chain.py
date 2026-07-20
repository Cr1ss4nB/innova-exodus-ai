import logging
from functools import lru_cache

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import get_settings
from app.core.exceptions import LLMGenerationError
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


def answer_question(question: str) -> tuple[str, list[RetrievedChunk]]:
    """Ejecuta el flujo RAG completo: recupera contexto, construye el prompt y consulta a Gemini."""
    chunks = retrieve_relevant_chunks(question)
    context = _build_context(chunks)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT_TEMPLATE),
            ("human", "{question}"),
        ]
    )
    chain = prompt | get_chat_model() | StrOutputParser()

    logger.info("Consultando a Gemini para la pregunta: '%s'", question)

    try:
        answer = chain.invoke({"context": context, "question": question})
    except Exception as error:
        raise LLMGenerationError("Fallo al generar la respuesta con el modelo de lenguaje") from error

    return answer, chunks
