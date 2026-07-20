from pydantic import BaseModel, Field

from app.models.chat import ChatAnswer


class ChatRequest(BaseModel):
    """Pregunta enviada por el usuario al asistente."""

    question: str = Field(..., min_length=1, description="Pregunta en lenguaje natural")


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
