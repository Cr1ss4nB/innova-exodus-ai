from app.models.chat import ChatTurn
from app.rag.chain import _build_retrieval_query


def test_returns_question_unchanged_without_history():
    assert _build_retrieval_query("¿Cuál es el horario?", []) == "¿Cuál es el horario?"


def test_prepends_previous_questions_when_history_exists():
    history = [
        ChatTurn(question="¿Cuál es el protocolo de incidentes?", answer="Es X, Y, Z."),
        ChatTurn(question="¿Y quién lo ejecuta?", answer="El equipo de seguridad."),
    ]

    result = _build_retrieval_query("¿Y qué más?", history)

    assert "¿Cuál es el protocolo de incidentes?" in result
    assert "¿Y quién lo ejecuta?" in result
    assert result.endswith("¿Y qué más?")
