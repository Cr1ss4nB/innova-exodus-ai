from pydantic import BaseModel, Field

from app.models.chat import ChatAnswer

MAX_HISTORY_TURNS = 3


class ChatHistoryTurn(BaseModel):
    """Un intercambio previo (pregunta + respuesta) de la conversación actual, enviado por el
    frontend para dar contexto. El backend no lo almacena en ningún momento."""

    question: str
    answer: str


class ChatRequest(BaseModel):
    """Pregunta enviada por el usuario al asistente, con un historial corto y opcional."""

    question: str = Field(..., min_length=1, description="Pregunta en lenguaje natural")
    history: list[ChatHistoryTurn] = Field(
        default_factory=list,
        max_length=MAX_HISTORY_TURNS,
        description="Últimos intercambios de la conversación actual, sin persistencia en el servidor",
    )


class SourceReference(BaseModel):
    """Referencia a un documento y página utilizados para construir la respuesta."""

    document: str
    page: int


class ChatResponse(BaseModel):
    """Respuesta generada por el asistente junto con las fuentes documentales utilizadas."""

    answer: str
    sources: list[SourceReference]

    @classmethod
    def from_answer(cls, chat_answer: ChatAnswer) -> "ChatResponse":
        return cls(
            answer=chat_answer.answer,
            sources=[
                SourceReference(document=source.document, page=source.page) for source in chat_answer.sources
            ],
        )
