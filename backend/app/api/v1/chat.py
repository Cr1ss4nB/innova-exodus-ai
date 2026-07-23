from fastapi import APIRouter

from app.models.chat import ChatTurn
from app.schemas.chat_schemas import ChatRequest, ChatResponse
from app.services.chat_service import ask

router = APIRouter(prefix="/chat")


@router.post("", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest) -> ChatResponse:
    """Responde una pregunta utilizando exclusivamente la documentación indexada en FAISS.

    El historial recibido es efímero: vive únicamente en el frontend durante la conversación
    actual y se reenvía en cada solicitud; el backend no lo almacena en ningún momento.
    """
    history = [ChatTurn(question=turn.question, answer=turn.answer) for turn in request.history]
    chat_answer = ask(request.question, history)
    return ChatResponse.from_answer(chat_answer)
