from dataclasses import dataclass


@dataclass
class ChatSource:
    """Fuente documental utilizada para construir una respuesta del chat."""

    document: str
    page: int


@dataclass
class ChatTurn:
    """Un intercambio previo (pregunta + respuesta) dentro de la conversación actual.

    Es efímero: lo aporta el frontend en cada solicitud y el backend nunca lo persiste.
    """

    question: str
    answer: str


@dataclass
class ChatAnswer:
    """Resultado del flujo RAG: la respuesta generada y las fuentes utilizadas."""

    answer: str
    sources: list[ChatSource]
