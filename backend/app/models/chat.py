from dataclasses import dataclass


@dataclass
class ChatSource:
    """Fuente documental utilizada para construir una respuesta del chat."""

    document: str
    page: int


@dataclass
class ChatAnswer:
    """Resultado del flujo RAG: la respuesta generada y las fuentes utilizadas."""

    answer: str
    sources: list[ChatSource]
